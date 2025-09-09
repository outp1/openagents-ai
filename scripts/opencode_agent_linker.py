#!/usr/bin/env python3
"""
Lightweight Markdown Agent Linker for opencode
Usage:
  link  -m path/to/agent.md [-c path/to/opencode.json] [-s global|project] [-a agent-id (optional)]
  unlink -a agent-id [-c path/to/opencode.json] [-s global|project]
  list  [-c path/to/opencode.json] [-s global|project]

Notes:
- This is a simplified linker that reads a Markdown file with a YAML-like front matter and
  writes a corresponding entry into a JSON opencode config under the top-level "agent" map.
- For now it operates on JSON configs only (JSONC support can be added later).
"""
import argparse
import json
import os
import re
import sys

FRONT_MATTER_START = '---'
FRONT_MATTER_END = '---'


def parse_front_matter(md_path: str):
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    start = None
    end = None
    for i, line in enumerate(lines):
        if line.strip() == FRONT_MATTER_START:
            if start is None:
                start = i
            else:
                end = i
                break
    if start is None or end is None or end <= start:
        raise ValueError(f"Markdown file {md_path} missing valid front matter between '---' blocks.")

    block = lines[start + 1:end]
    data = {}
    inside_tools = False
    for line in block:
        s = line.rstrip('\n')
        if not s.strip():
            continue
        if s.strip().startswith('tools:'):
            inside_tools = True
            data['tools'] = {}
            continue
        if not inside_tools:
            m = re.match(r'^([A-Za-z_][\w-]*)\s*:\s*(.*)$', s.strip())
            if m:
                key = m.group(1)
                val = m.group(2).strip()
                if val.lower() == 'true':
                    val = True
                elif val.lower() == 'false':
                    val = False
                elif val.startswith('"') and val.endswith('"'):
                    val = val[1:-1]
                data[key] = val
        else:
            m = re.match(r'^[\s]*([A-Za-z_][\w-]*)\s*:\s*(.*)$', s)
            if m:
                k = m.group(1)
                v = m.group(2).strip()
                if v.lower() == 'true':
                    v = True
                elif v.lower() == 'false':
                    v = False
                elif v.startswith('"') and v.endswith('"'):
                    v = v[1:-1]
                data['tools'][k] = v
    if 'id' not in data:
        raise ValueError("Front matter missing 'id' field")
    if 'model' not in data:
        raise ValueError("Front matter missing 'model' field")
    if 'prompt' not in data:
        raise ValueError("Front matter missing 'prompt' field")
    if 'name' not in data:
        data['name'] = data['id']
    return data


def agent_from_markdown(md_path: str) -> dict:
    meta = parse_front_matter(md_path)
    agent = {
        'id': meta['id'],
        'name': meta.get('name', meta['id']),
        'description': meta.get('description', ''),
        'model': meta['model'],
        'prompt': meta['prompt'],
        'tools': meta.get('tools', {})
    }
    return agent


def load_config(config_path: str) -> dict:
    if not os.path.exists(config_path):
        # create basic skeleton
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        data = {"$schema": "https://opencode.ai/config.json", "agent": {}}
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        return data
    with open(config_path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            raise ValueError(f"Config at {config_path} is not valid JSON.")


def save_config(config_path: str, data: dict):
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def main():
    ap = argparse.ArgumentParser(prog='opencode_agent_linker', description='Link Markdown-defined agents into opencode.json')
    sub = ap.add_subparsers(dest='cmd', required=True)

    sp_link = sub.add_parser('link', help='Link a Markdown agent into config')
    sp_link.add_argument('-m', '--markdown', required=True, help='Path to agent markdown file')
    sp_link.add_argument('-c', '--config', required=False, help='Path to opencode.json (project or global)')
    sp_link.add_argument('-s', '--scope', choices=['global', 'project'], default='project')
    sp_link.add_argument('-a', '--agent-id', required=False, help='Optional explicit agent id (overrides in markdown)')

    sp_unlink = sub.add_parser('unlink', help='Unlink an agent from config')
    sp_unlink.add_argument('-a', '--agent-id', required=True, help='Agent id to unlink')
    sp_unlink.add_argument('-c', '--config', required=False, help='Path to opencode.json')
    sp_unlink.add_argument('-s', '--scope', choices=['global', 'project'], default='project')

    sp_list = sub.add_parser('list', help='List linked agents in config')
    sp_list.add_argument('-c', '--config', required=False, help='Path to opencode.json')
    sp_list.add_argument('-s', '--scope', choices=['global', 'project'], default='project')

    ns = ap.parse_args()

    # Resolve config path
    if ns.cmd == 'link':
        md_path = os.path.abspath(ns.markdown)
        if not os.path.exists(md_path):
            print(f"Markdown agent not found: {md_path}")
            sys.exit(2)
        agent = agent_from_markdown(md_path)
        if ns.agent_id:
            agent['id'] = ns.agent_id
        agent_id = agent['id']
        # Resolve config path
        if ns.config:
            config_path = os.path.abspath(ns.config)
        else:
            if ns.scope == 'global':
                config_path = os.path.expanduser('~/.config/opencode/opencode.json')
            else:
                # project: default to opencode.json in CWD or a config/opencode.json
                cwd = os.getcwd()
                if os.path.exists(os.path.join(cwd, 'opencode.json')):
                    config_path = os.path.join(cwd, 'opencode.json')
                else:
                    config_path = os.path.join(cwd, 'config', 'opencode.json')
        data = load_config(config_path)
        if 'agent' not in data or not isinstance(data['agent'], dict):
            data['agent'] = {}
        data['agent'][agent_id] = agent
        save_config(config_path, data)
        print(f"Linked agent '{agent_id}' to {config_path}")
        return

    if ns.cmd == 'unlink':
        if ns.config:
            config_path = os.path.abspath(ns.config)
        else:
            if ns.scope == 'global':
                config_path = os.path.expanduser('~/.config/opencode/opencode.json')
            else:
                cwd = os.getcwd()
                if os.path.exists(os.path.join(cwd, 'opencode.json')):
                    config_path = os.path.join(cwd, 'opencode.json')
                else:
                    config_path = os.path.join(cwd, 'config', 'opencode.json')
        data = load_config(config_path)
        if 'agent' in data and ns.agent_id in data['agent']:
            del data['agent'][ns.agent_id]
            save_config(config_path, data)
            print(f"Unlinked agent '{ns.agent_id}' from {config_path}")
        else:
            print(f"Agent '{ns.agent_id}' not found in {config_path}")
        return

    if ns.cmd == 'list':
        if ns.config:
            config_path = os.path.abspath(ns.config)
        else:
            if ns.scope == 'global':
                config_path = os.path.expanduser('~/.config/opencode/opencode.json')
            else:
                cwd = os.getcwd()
                if os.path.exists(os.path.join(cwd, 'opencode.json')):
                    config_path = os.path.join(cwd, 'opencode.json')
                else:
                    config_path = os.path.join(cwd, 'config', 'opencode.json')
        data = load_config(config_path)
        agents = data.get('agent', {}) if isinstance(data, dict) else {}
        print(f"Agents linked in {config_path}:")
        for aid in sorted(agents.keys()):
            ai = agents[aid]
            name = ai.get('name', aid)
            print(f"- {aid}: {name}")
        return

    print("No command executed.")


if __name__ == '__main__':
    main()
