"""Deliberately imperfect local evaluation fixture; not production software."""

import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=Path, required=True)
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add")
    add.add_argument("title")
    listing = commands.add_parser("list")
    listing.add_argument("--all", action="store_true")
    archive = commands.add_parser("archive")
    archive.add_argument("id", type=int)
    commands.add_parser("stats")
    export = commands.add_parser("export")
    export.add_argument("--status", choices=("active", "all"), default="active")
    show = commands.add_parser("show")
    show.add_argument("id", type=int)
    args = parser.parse_args()
    tasks = json.loads(args.db.read_text()) if args.db.exists() else []
    if args.command == "add":
        task = {"id": max((t["id"] for t in tasks), default=0) + 1,
                "title": args.title, "archived": False}
        tasks.append(task)
        print(json.dumps({"message": "Saved", "task": task}))
    elif args.command == "list":
        print(json.dumps(tasks if args.all else [t for t in tasks if not t["archived"]]))
    elif args.command == "archive":
        for task in tasks:
            if task["id"] == args.id:
                task["archived"] = True
                args.db.write_text(json.dumps(tasks))
                print(json.dumps({"message": "Archived", "id": args.id}))
                return
        parser.exit(1, "Task not found\n")
    elif args.command == "stats":
        print(json.dumps({"active": len(tasks), "total": len(tasks)}))
    elif args.command == "export":
        print(json.dumps({"tasks": tasks, "status": args.status}))
    elif args.command == "show":
        task = next((t for t in tasks if t["id"] == args.id), None)
        print(json.dumps(task if task else {"error": "Task not found"}))


if __name__ == "__main__":
    main()
