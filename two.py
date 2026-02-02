import os
import subprocess
import random
from datetime import datetime, timedelta
from time import sleep

def neon_ascii_banner():
    banner = r"""
███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗ ██████╗  ██████╗ ██╗  ██╗███████╗██████╗ ███████╗
████╗  ██║██╔════╝██║ ██╔╝╚██╗ ██╔╝██╔════╝██╔═══██╗██╔════╝ ██║  ██║██╔════╝██╔══██╗██╔════╝
██╔██╗ ██║█████╗  █████╔╝  ╚████╔╝ █████╗  ██║   ██║██║  ███╗███████║█████╗  ██████╔╝███████╗
██║╚██╗██║██╔══╝  ██╔═██╗   ╚██╔╝  ██╔══╝  ██║   ██║██║   ██║██╔══██║██╔══╝  ██╔═══╝ ╚════██║
██║ ╚████║███████╗██║  ██╗   ██║   ███████╗╚██████╔╝╚██████╔╝██║  ██║███████╗██║     ███████║
╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝     ╚══════╝
                              BY: NexusGK Softwares 🚀
    """
    print(f"\033[95m{banner}\033[0m")

def ask_input(prompt_text, default=None):
    value = input(f"{prompt_text} [{default}]: ") if default else input(f"{prompt_text}: ")
    return value.strip() or default

def loading_bar(task, duration=3):
    print(f"\n{task}...", end="", flush=True)
    for i in range(30):
        print("█", end="", flush=True)
        sleep(duration / 30)
    print(" ✅")

def generate_commits(repo_path, remote_url, start_date, end_date, commits_per_day):
    if not os.path.exists(repo_path):
        os.mkdir(repo_path)
        subprocess.run(["git", "init"], cwd=repo_path)

    # Clean up possible previous crash
    commit_msg_file = os.path.join(repo_path, ".git", "COMMIT_EDITMSG")
    if os.path.exists(commit_msg_file):
        os.remove(commit_msg_file)

    # Git user config (optional)
    subprocess.run(["git", "config", "user.name", "Fake Commit Bot"], cwd=repo_path)
    subprocess.run(["git", "config", "user.email", "bot@nexusgk.dev"], cwd=repo_path)

    print("\n🛠️  Generating commits...")
    date = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    total_days = (end - date).days + 1
    total_commits = 0

    for day in range(total_days):
        daily_commits = random.randint(1, 5) if commits_per_day == 'random' else int(commits_per_day)

        for i in range(daily_commits):
            with open(os.path.join(repo_path, "file.txt"), "a") as f:
                f.write(f"{date} - Commit {i}\n")
            env = os.environ.copy()
            commit_time = f"{date.strftime('%Y-%m-%d')}T12:00:00"
            env["GIT_AUTHOR_DATE"] = commit_time
            env["GIT_COMMITTER_DATE"] = commit_time
            subprocess.run(["git", "add", "."], cwd=repo_path)
            subprocess.run(["git", "commit", "-m", f"Commit {i} on {date.date()}"], cwd=repo_path, env=env)
            total_commits += 1

        date += timedelta(days=1)

    loading_bar("📤 Pushing commits to GitHub")

    # Remove origin if exists
    subprocess.run(["git", "remote", "remove", "origin"], cwd=repo_path)
    subprocess.run(["git", "remote", "add", "origin", remote_url], cwd=repo_path)
    subprocess.run(["git", "branch", "-M", "main"], cwd=repo_path)
    subprocess.run(["git", "push", "-u", "origin", "main"], cwd=repo_path)

    print(f"\n✅ {total_commits} commits successfully pushed to GitHub!")

# === MAIN ===
if __name__ == "__main__":
    neon_ascii_banner()
    print("🔥 GitHub Fake Commit Generator CLI 🔥\n")

    repo_name = ask_input("Enter a folder name for your fake commit repo", "fake-commits")
    repo_path = repo_name if os.path.isabs(repo_name) else os.path.join(".", repo_name)

    remote_url = ask_input("Enter your GitHub repo URL (must be created first)")
    start_date = ask_input("Enter start date (YYYY-MM-DD)")
    end_date = ask_input("Enter end date (YYYY-MM-DD)")
    commits_per_day = ask_input("Commits per day (or type 'random')", "random")

    generate_commits(repo_path, remote_url, start_date, end_date, commits_per_day)