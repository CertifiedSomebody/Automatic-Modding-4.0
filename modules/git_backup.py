import os
import shutil
import subprocess
from datetime import datetime


# -------------------------------------------------
# Run git command safely
# -------------------------------------------------
def run_git_command(repo_path, command):

    result = subprocess.run(
        command,
        cwd=repo_path,
        shell=True,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise Exception(result.stderr.strip())

    return result.stdout.strip()


# -------------------------------------------------
# Copy files into repo (overwrite)
# -------------------------------------------------
def copy_files_to_repo(files, repo_path):

    if not os.path.exists(repo_path):
        raise Exception("Repository folder does not exist")

    copied_files = []

    for file_path in files:

        if not os.path.isfile(file_path):
            continue

        filename = os.path.basename(file_path)
        dest_path = os.path.join(repo_path, filename)

        shutil.copy2(file_path, dest_path)

        copied_files.append(filename)

    if not copied_files:
        raise Exception("No valid files selected")

    return copied_files


# -------------------------------------------------
# Create commit message
# -------------------------------------------------
def create_commit_message(files):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    file_list = ", ".join(files)

    return f"Auto Backup [{timestamp}] - {file_list}"


# -------------------------------------------------
# Main backup function
# -------------------------------------------------
def backup_to_git(files, repo_path):

    # Copy files first
    copied_files = copy_files_to_repo(files, repo_path)

    # Git add
    run_git_command(repo_path, "git add .")

    # Commit
    commit_msg = create_commit_message(copied_files)

    try:
        run_git_command(
            repo_path,
            f'git commit -m "{commit_msg}"'
        )
    except Exception as e:

        # Nothing to commit case
        if "nothing to commit" in str(e).lower():
            return {
                "status": "No changes",
                "files": copied_files
            }
        else:
            raise e

    # Push
    run_git_command(repo_path, "git push")

    return {
        "status": "Success",
        "files": copied_files,
        "message": commit_msg
    }