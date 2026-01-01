import os
import subprocess
import random
from datetime import datetime, timedelta
from time import sleep

# ==============================
#   NEXUSGK SOFTWARES 🚀
#   GitHub Commit Generator
# ==============================

def neon_ascii_banner():
    banner = r"""
███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗ ██████╗  ██████╗ ██╗  ██╗███████╗██████╗ ███████╗
████╗  ██║██╔════╝██║ ██╔╝╚██╗ ██╔╝██╔════╝██╔═══██╗██╔════╝ ██║  ██║██╔════╝██╔══██╗██╔════╝
██╔██╗ ██║█████╗  █████╔╝  ╚████╔╝ █████╗  ██║   ██║██║  ███╗███████║█████╗  ██████╔╝███████╗
██║╚██╗██║██╔══╝  ██╔═██╗   ╚██╔╝  ██╔══╝  ██║   ██║██║   ██║██╔══██║██╔══╝  ██╔═══╝ ╚════██║
██║ ╚████║███████╗██║  ██╗   ██║   ███████╗╚██████╔╝╚██████╔╝██║  ██║███████╗██║     ███████║
╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝     ╚══════╝

                         🚀 NEXUSGK SOFTWARES 🚀
"""
    print(f"\033[95m{banner}\033[0m")


def ask_input(prompt_text, default=None):
    value = input(f"{prompt_text} [{default}]: ") if default else input(f"{prompt_text}: ")
    return value.strip() or default


def loading_bar(task, duration=3):
    print(f"\n{task}")
    for i in range(31):
        percent = int((i / 30) * 100)
        bar = "█" * i + "-" * (30 - i)
        print(f"\r[{bar}] {percent}%", end="", flush=True)
        sleep(duration / 30)
    print(" ✅\n")


def run_git_command(command, cwd, env=None):
    subprocess.run(
        command,
        cwd=cwd,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def generate_commits(repo_path, remote_url, start_date, end_date, commits_per_day):

    # ==========================
    # CREATE REPO IF NOT EXISTS
    # ==========================
    if not os.path.exists(repo_path):
        os.mkdir(repo_path)
        run_git_command(["git", "init"], cwd=repo_path)

    # ==========================
    # REMOVE LOCK FILES
    # ==========================
    lock_file = os.path.join(repo_path, ".git", "index.lock")
    commit_msg_file = os.path.join(repo_path, ".git", "COMMIT_EDITMSG")

    if os.path.exists(lock_file):
        os.remove(lock_file)

    if os.path.exists(commit_msg_file):
        os.remove(commit_msg_file)

    # ==========================
    # GIT CONFIG
    # ==========================
    run_git_command(
        ["git", "config", "user.name", "NexusGKSoftwares"],
        cwd=repo_path
    )

    run_git_command(
        ["git", "config", "user.email", "nexusgk3@gmail.com"],
        cwd=repo_path
    )

    # ==========================
    # DATE SETUP
    # ==========================
    date = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    # Prevent future date issues
    today = datetime.now()

    if end > today:
        print("\n⚠️ End date is in the future.")
        print("⚡ GitHub may not count future contributions properly.")
        print(f"📅 Auto-adjusting end date to today ({today.strftime('%Y-%m-%d')})\n")
        end = today

    total_days = (end - date).days + 1
    total_commits = 0

    print("\n🛠️ Generating commits...\n")

    # ==========================
    # GENERATE COMMITS
    # ==========================
    while date <= end:

        # Always at least 1 commit
        daily_commits = (
            random.randint(1, 8)
            if commits_per_day.lower() == "random"
            else max(1, int(commits_per_day))
        )

        print(f"📅 {date.strftime('%Y-%m-%d')} → {daily_commits} commits")

        for i in range(daily_commits):

            # Modify file
            file_path = os.path.join(repo_path, "activity.txt")

            with open(file_path, "a") as f:
                f.write(
                    f"Commit {i} on {date.strftime('%Y-%m-%d')} "
                    f"at {datetime.now()}\n"
                )

            # Random realistic commit time
            hour = random.randint(8, 23)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)

            commit_time = (
                f"{date.strftime('%Y-%m-%d')}T"
                f"{hour:02}:{minute:02}:{second:02}"
            )

            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"] = commit_time
            env["GIT_COMMITTER_DATE"] = commit_time

            # Git add
            run_git_command(
                ["git", "add", "."],
                cwd=repo_path
            )

            # Git commit
            subprocess.run(
                [
                    "git",
                    "commit",
                    "--no-gpg-sign",
                    "-m",
                    f"Commit {i} on {date.strftime('%Y-%m-%d')}"
                ],
                cwd=repo_path,
                env=env,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            total_commits += 1

        date += timedelta(days=1)

    # ==========================
    # PUSH TO GITHUB
    # ==========================
    loading_bar("📤 Pushing commits to GitHub", 4)

    # Remove origin if exists
    subprocess.run(
        ["git", "remote", "remove", "origin"],
        cwd=repo_path,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Add origin
    run_git_command(
        ["git", "remote", "add", "origin", remote_url],
        cwd=repo_path
    )

    # Main branch
    run_git_command(
        ["git", "branch", "-M", "main"],
        cwd=repo_path
    )

    # Push
    subprocess.run(
        ["git", "push", "-u", "origin", "main", "--force"],
        cwd=repo_path
    )

    print("\n===================================")
    print(f"✅ SUCCESSFULLY PUSHED {total_commits} COMMITS")
    print("🚀 GitHub contribution graph updated!")
    print("===================================\n")


# ==========================
# MAIN
# ==========================
if __name__ == "__main__":

    os.system("clear" if os.name != "nt" else "cls")

    neon_ascii_banner()

    print("🔥 GitHub Contribution Generator 🔥")
    print("💚 Fill your GitHub graph with commits\n")

    repo_name = ask_input(
        "Enter local repo folder name",
        "fake-commits"
    )

    repo_path = (
        repo_name
        if os.path.isabs(repo_name)
        else os.path.join(".", repo_name)
    )

    remote_url = ask_input(
        "Enter GitHub repo URL"
    )

    # 2026-aware defaults
    start_date = ask_input(
        "Enter start date (YYYY-MM-DD)",
        "2026-01-01"
    )

    end_date = ask_input(
        "Enter end date (YYYY-MM-DD)",
        datetime.now().strftime("%Y-%m-%d")
    )

    commits_per_day = ask_input(
        "Commits per day ('random' or number)",
        "random"
    )

    generate_commits(
        repo_path,
        remote_url,
        start_date,
        end_date,
        commits_per_day
    )