# Gitlab2Github
Simple cli app to help mirroring repositories from GitLab to Github

## Command
### GitHub
* Check if repository exists
```shell
python3 -m gitlab2github github repo check <repo_name>
```
* Create repository
```shell
python3 -m gitlab2github github repo create <repo_name>
```

## How to use
Create Acces tokens to communicate with repository and use environment variables to access to repository:
| Name | Description |
|------|-------------|
| GH_TOKEN | A GitHub [personal access token](https://docs.github.com/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).
| GH_USER | GitHub repository owner
| GL_TOKEN | A GitLab [personal access token](https://docs.gitlab.com/ce/user/profile/personal_access_tokens.html).
| GL_USER | GitLab repository owner


Example:
```shell
# Set environment
export GH_USER=artem-shestakov
export GH_TOKEN=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
export GL_USER=artem-shestakov
export GL_TOKEN=glpat-nJ3PxzaS7im8xBnJyS6a

# Create push mirror from GitLab project id 42771718 to GitHub
python3 -m gitlab2github mirror 42771718 GitLab2GitHub
🚧 Repository "gitlab2github" is being created...
🚀 Repository "gitlab2github" was created
🪞 Mirror for "gitlab2github" is being created...
👍 Mirror for "gitlab2github" was created
```