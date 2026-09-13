#!/usr/bin/env bash
# Deterministic STRUCTURAL validation for the Qortal development workspace.
#
# Scope (structural only):
#   1. required workspace files exist;
#   2. supported relative Markdown link forms resolve:
#        - inline links:          [text](path) / [text](path#anchor)
#        - reference definitions: [label]: path
#      and local heading anchors resolve to a heading in the target file;
#   3. a small hard-coded stale-platform marker is absent from ACTIVE guidance
#      (historical reports are excluded, so quoting an old assumption inside an
#      audit/report cannot cause a false hard failure);
#   4. a hygiene report of terms that need human review (warn only).
#
# This checker is NOT semantic proof of platform correctness. It does not prove
# that bridge contracts, authority rules or security guidance are correct;
# semantic/source review remains a separate mandatory gate.
#
# Usage: bash tools/validate-workspace.sh
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)" \
  || { printf 'FATAL: cannot resolve workspace root\n' >&2; exit 2; }
cd "$ROOT" || { printf 'FATAL: cannot cd to %s\n' "$ROOT" >&2; exit 2; }

fail=0
warn=0

say()  { printf '%s\n' "$*"; }
ok()   { printf '  ok   %s\n' "$*"; }
bad()  { printf '  FAIL %s\n' "$*"; fail=$((fail + 1)); }
note() { printf '  warn %s\n' "$*"; warn=$((warn + 1)); }

say "Qortal workspace validation (structural)"
say "root: $ROOT"
say ""

say "[1] required files"
required=(
  README.md
  AGENTS.md
  agents/README.md
  agents/00-SESSION-START.md
  agents/01-TASK-CLASSIFICATION.md
  agents/qortal-native-app-workflow.md
  agents/qortal-architecture-and-data-integrity.md
  agents/qortal-qdn-and-bridge.md
  agents/qdn-publication-discovery-and-scaling.md
  agents/runtime-diagnostics-and-performance.md
  agents/live-qdn-validation.md
  agents/issue-driven-audit-and-refactor.md
  agents/app-release-and-provenance.md
  agents/git-generated-files-and-hygiene.md
  agents/final-report-and-owner-handoff.md
  agents/roles/CHATGPT.md
  agents/roles/DEEPSEEK.md
  agents/roles/CODEX.md
  docs/architecture/qortal-dapp-development-standard.md
  docs/governance/source-of-truth-and-lifecycle.md
  docs/workflows/workflow-v2.md
  docs/workflows/deepseek-primary-work-model.md
  docs/workflows/report-storage-policy.md
  projects/shadow-archives-webportal.md
  templates/TASK-CONTROLLER.md
  templates/PROJECT-CONTEXT.md
  templates/AUDIT-ISSUE.md
  templates/IMPLEMENTATION-ISSUE.md
  templates/OWNER-HANDOFF.md
  templates/DEEPSEEK-TASK.md
  templates/DEEPSEEK-REVIEW.md
  tools/validate-workspace.sh
)
for f in "${required[@]}"; do
  if [[ -f "$f" ]]; then ok "$f"; else bad "missing $f"; fi
done
say ""

say "[2] relative Markdown links and local anchors"
mdlist="$(find . -type f -name '*.md' -not -path './.git/*' -not -path '*/node_modules/*' | sort)" \
  || bad "Markdown file enumeration failed"
if [[ -z "$mdlist" ]]; then
  bad "no Markdown files found"
fi
mapfile -t mdfiles <<< "$mdlist"

# Historical reports are evidence, not active guidance. Quoting an obsolete
# assumption inside them must not create a false hard failure.
is_historical() {
  case "$1" in
    ./docs/*/audits/*|./docs/*/bootstrap/*|./docs/*/issues/*|./docs/*/reviews/*|\
./docs/*/implementations/*|./docs/*/investigations/*|./docs/*/runtime/*|\
./docs/*/validation/*|./docs/*/handoffs/*|./docs/*/remediation/*) return 0 ;;
    *) return 1 ;;
  esac
}

# GitHub-style heading slug candidates, including duplicate suffixes
# (heading, heading-1, heading-2, ...).
anchors_of() {
  local file="$1"
  awk '
    /^#{1,6}[ \t]+/ {
      line = $0
      sub(/^#{1,6}[ \t]+/, "", line)
      sub(/[ \t]+#+[ \t]*$/, "", line)
      line = tolower(line)
      gsub(/[^a-z0-9 _-]/, "", line)
      gsub(/ /, "-", line)
      if (line != "") print line
    }
  ' "$file"
  grep -oE '\{#[A-Za-z0-9._-]+\}' "$file" 2>/dev/null | sed -E 's/^\{#//; s/\}$//' || true
}

anchor_exists() {
  local file="$1" want="$2"
  [[ -n "$want" ]] || return 0
  anchors_of "$file" \
    | awk '{c[$0]++; if (c[$0]==1) print $0; else print $0"-"(c[$0]-1)}' \
    | grep -qxF "$want"
}

link_errors=0
checked=0
anchor_checked=0
for f in "${mdfiles[@]}"; do
  [[ -n "$f" ]] || continue
  dir="$(dirname "$f")"

  dests="$(
    { grep -oE '\]\([^)]+\)' "$f" 2>/dev/null | sed -E 's/^\]\(//; s/\)$//' || true
      grep -E '^ {0,3}\[[^]]+\]:' "$f" 2>/dev/null \
        | sed -E 's/^[[:space:]]*\[[^]]+\]:[[:space:]]*<?([^ >]+)>?.*$/\1/' || true
    } | sed -E 's/^<//; s/>$//'
  )"
  [[ -n "$dests" ]] || continue

  while IFS= read -r raw; do
    [[ -n "$raw" ]] || continue

    target="$raw"
    anchor=""
    if [[ "$target" == *"#"* ]]; then
      anchor="${target##*#}"
      target="${target%%#*}"
    fi
    target="${target%% *}"

    case "$target" in
      http://*|https://*|mailto:*|tel:*|qortal://*) continue ;;
    esac

    if [[ -z "$target" ]]; then
      # Same-file anchor.
      if [[ -n "$anchor" ]]; then
        anchor_checked=$((anchor_checked + 1))
        if ! anchor_exists "$f" "$anchor"; then
          bad "$f -> #$anchor (missing heading anchor in $f)"
          link_errors=$((link_errors + 1))
        fi
      fi
      continue
    fi

    checked=$((checked + 1))
    resolved="$dir/$target"
    if [[ ! -e "$resolved" ]]; then
      bad "$f -> $target"
      link_errors=$((link_errors + 1))
      continue
    fi
    if [[ -n "$anchor" && "$target" == *.md ]]; then
      anchor_checked=$((anchor_checked + 1))
      if ! anchor_exists "$resolved" "$anchor"; then
        bad "$f -> $target#$anchor (missing heading anchor)"
        link_errors=$((link_errors + 1))
      fi
    fi
  done <<< "$dests"
done
say "  checked $checked relative links and $anchor_checked anchors across ${#mdfiles[@]} files"
if [[ "$link_errors" -eq 0 ]]; then ok "all supported relative links and anchors resolve"; fi
say ""

say "[3] stale platform assumptions in active guidance (hard fail)"
stale_hits=0
for f in "${mdfiles[@]}"; do
  [[ -n "$f" ]] || continue
  is_historical "$f" && continue
  if out="$(grep -n '24891' "$f")"; then
    printf '%s\n' "$out" | sed "s#^#       $f:#"
    stale_hits=$((stale_hits + 1))
  else
    rc=$?
    [[ "$rc" -gt 1 ]] && bad "grep failed while scanning $f (exit $rc)"
  fi
done
if [[ "$stale_hits" -eq 0 ]]; then
  ok "no 24891 endpoint references in active guidance"
else
  bad "found Qortium preview endpoint 24891 in $stale_hits active file(s)"
fi
say ""

say "[4] hygiene scan (review)"
scan() {
  local pattern="$1" label="$2" hits
  hits="$(
    for f in "${mdfiles[@]}"; do
      [[ -n "$f" ]] || continue
      is_historical "$f" && continue
      grep -HniE "$pattern" "$f" 2>/dev/null || true
    done
  )"
  if [[ -n "$hits" ]]; then
    note "$label"
    printf '%s\n' "$hits" | sed 's/^/       /' | head -40
  else
    ok "no $label"
  fi
}
scan '\bqortium\b' 'Qortium references (expected only in migration/provenance/comparison notes)'
scan 'ssh' 'SSH references (review against universal environment policy)'
scan 'qavs' 'QAVS references (expected only in the explicit "no QAVS" note)'
scan '12391|62391' 'node API port references (must be environment-scoped, not asserted as universal)'
scan 'qortal-ui' 'legacy qortal-ui references (must be marked archived/non-authoritative)'
say ""

say "result"
if [[ "$fail" -eq 0 ]]; then
  say "PASS (${warn} warnings for human review)"
  exit 0
else
  say "FAIL (${fail} errors, ${warn} warnings)"
  exit 1
fi
