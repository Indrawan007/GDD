#!/usr/bin/env python3
"""Lint ringan untuk proyek Godot greybox.

Bukan pengganti parser Godot — ini menangkap kelas kesalahan yang paling sering
terjadi saat file ditulis tanpa bisa menjalankan engine:

  1. tanda kurung tidak seimbang
  2. indentasi campur tab/spasi
  3. `load()/preload()` menunjuk file yang tidak ada
  4. signal EventBus yang dipakai tapi tidak dideklarasikan
  5. konstanta Tuning yang dipakai tapi tidak ada
  6. `$Node` @onready yang tidak pernah dibuat di file yang sama
  7. nama fungsi ganda dalam satu file

Jalankan: python3 tools/lint_gdscript.py
"""

from __future__ import annotations

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME = os.path.join(ROOT, "game")

errors: list[str] = []
warnings: list[str] = []


def rel(p: str) -> str:
    return os.path.relpath(p, ROOT)


def strip_code(line: str) -> str:
    """Buang komentar & isi string (kasar tapi cukup untuk cek tanda kurung)."""
    out = []
    in_str: str | None = None
    i = 0
    while i < len(line):
        ch = line[i]
        if in_str:
            if ch == "\\":
                i += 2
                continue
            if ch == in_str:
                in_str = None
            i += 1
            continue
        if ch in "\"'":
            in_str = ch
            i += 1
            continue
        if ch == "#":
            break
        out.append(ch)
        i += 1
    return "".join(out)


def check_balance(path: str, text: str) -> None:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []
    for ln, line in enumerate(text.splitlines(), 1):
        for ch in strip_code(line):
            if ch in "([{":
                stack.append(ch)
            elif ch in ")]}":
                if not stack or stack[-1] != pairs[ch]:
                    errors.append(f"{rel(path)}:{ln}: kurung '{ch}' tidak cocok")
                    return
                stack.pop()
    if stack:
        errors.append(f"{rel(path)}: kurung tidak tertutup: {''.join(stack)}")


def check_indent(path: str, text: str) -> None:
    for ln, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        if line.startswith(" ") and not line.startswith("\t"):
            warnings.append(f"{rel(path)}:{ln}: indentasi spasi (proyek ini pakai tab)")
            return



def untyped_members_of(path: str, text: str) -> set[str]:
    """Semua variabel (member maupun lokal) yang dideklarasikan tanpa tipe = Variant."""
    names: set[str] = set()
    for m in re.finditer(r"^\s*var\s+(\w+)\s*(.*)$", text, re.M):
        rest = m.group(2)
        head = rest.split("=")[0]
        if not head.strip() and "=" not in rest:      # `var x` tanpa nilai
            names.add(m.group(1))
        elif "=" in rest and ":" not in head:          # `var x = ...` tanpa tipe
            names.add(m.group(1))
    return names


def untyped_hits(expr: str, untyped: set[str], path: str) -> str:
    for name in untyped:
        if re.search(r"\b__SELF__\b|\b" + re.escape(name) + r"\b", expr):
            return name
    return ""


def check_paths(path: str, text: str) -> None:
    for ln, line in enumerate(text.splitlines(), 1):
        for m in re.finditer(r'(load|preload)\("(res://[^"]+)"\)', line):
            target = os.path.join(GAME, m.group(2).replace("res://", ""))
            if not os.path.exists(target):
                errors.append(f"{rel(path)}:{ln}: aset tidak ada → {m.group(2)}")


def read(relpath: str) -> str:
    p = os.path.join(GAME, relpath)
    return open(p, encoding="utf-8").read()


def main() -> int:
    gd_files = []
    for base, _dirs, files in os.walk(GAME):
        for f in files:
            if f.endswith(".gd"):
                gd_files.append(os.path.join(base, f))

    if not gd_files:
        errors.append("tidak ada file .gd ditemukan")
        return report()

    # --- kumpulkan deklarasi global ---
    bus = read("scripts/autoload/event_bus.gd")
    signals = set(re.findall(r"^signal\s+(\w+)", bus, re.M))

    tuning = read("scripts/autoload/tuning.gd")
    consts = set(re.findall(r"^const\s+(\w+)", tuning, re.M))

    for path in gd_files:
        text = open(path, encoding="utf-8").read()
        check_balance(path, text)
        check_indent(path, text)
        check_paths(path, text)

        # fungsi ganda
        funcs = re.findall(r"^func\s+(\w+)", text, re.M)
        dupes = {f for f in funcs if funcs.count(f) > 1}
        for d in sorted(dupes):
            errors.append(f"{rel(path)}: fungsi '{d}' dideklarasikan lebih dari sekali")

        untyped_members = untyped_members_of(path, text)

        # signal bus
        for ln, line in enumerate(text.splitlines(), 1):
            for m in re.finditer(r'EventBus\.emit_signal\("(\w+)"', line):
                if m.group(1) not in signals:
                    errors.append(f"{rel(path)}:{ln}: sinyal EventBus '{m.group(1)}' tidak ada")
            for m in re.finditer(r"EventBus\.(\w+)\.(emit|connect)\(", line):
                if m.group(1) not in signals:
                    errors.append(f"{rel(path)}:{ln}: sinyal EventBus '{m.group(1)}' tidak ada")

            # konstanta Tuning
            for m in re.finditer(r"\bTuning\.([A-Z_][A-Z0-9_]*)", line):
                if m.group(1) not in consts:
                    errors.append(f"{rel(path)}:{ln}: konstanta Tuning.{m.group(1)} tidak ada")

            # GDScript tidak punya `x in (A, B)` seperti Python
            if re.search(r"\bin\s*\(", line):
                errors.append(
                    f"{rel(path)}:{ln}: `in (A, B)` bukan GDScript — pakai `or` / Array")

            # `:=` dari ekspresi yang menyentuh variabel/fungsi untyped (Variant)
            m_assign = re.match(r"\s*var\s+\w+\s*:=\s*(.+)$", line)
            if m_assign and untyped_hits(m_assign.group(1), untyped_members, path):
                errors.append(
                    f"{rel(path)}:{ln}: `:=` tidak bisa menginfer tipe dari ekspresi Variant "
                    f"({untyped_hits(m_assign.group(1), untyped_members, path)}) — tulis tipe eksplisit")

        # $Node yang dibuat di file yang sama
        built = set(re.findall(r'\.name\s*=\s*"(\w+)"', text))
        built |= set(re.findall(r'^\s*var\s+\w+\s*:?=\s*(\w+)\.new\(\)', text, re.M))
        for ln, line in enumerate(text.splitlines(), 1):
            for m in re.finditer(r"@onready\s+var\s+\w+\s*:\s*[\w\[\]]+\s*=\s*\$(\w+)", line):
                node = m.group(1)
                if node not in built and node not in {"Sprite", "Shadow", "Weapon", "Camera2D"}:
                    warnings.append(f"{rel(path)}:{ln}: ${node} tidak dibuat di file ini")

    return report()


def report() -> int:
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"\n{len(errors)} error · {len(warnings)} warning · "
          f"{len([1 for b, _d, fs in os.walk(GAME) for f in fs if f.endswith('.gd')])} file .gd")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
