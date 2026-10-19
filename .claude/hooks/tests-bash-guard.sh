#!/usr/bin/env bash
# PreToolUse guard for the tests subagent: only plain pytest invocations may run.
# Exit 2 blocks the tool call and shows stderr to the subagent.
cmd=$(jq -r '.tool_input.command // ""')

if [[ "$cmd" == *$'\n'* ]]; then
  echo "tests agent: multi-line commands are not allowed" >&2
  exit 2
fi

re='^(python3? -m )?pytest( [^;&|`$<>()\\]*)?$'
if [[ "$cmd" =~ $re ]]; then
  exit 0
fi
echo "tests agent: only 'pytest ...' or 'python[3] -m pytest ...' is allowed; got: $cmd" >&2
exit 2
