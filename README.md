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
Create Acces token to communicate with repository. Use environment variables to access to repository:
| Name | Description |
|------|-------------|
| GH_TOKEN | A GitHub [personal access token](https://docs.github.com/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).
| GH_USER | GitHub repository owner

Examples:
```shell
# Set environment
export GH_USER=artem-shestakov
export GH_TOKEN=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

# Create repository my-repo
python3 -m gitlab2github github repo create my-repo
```
or use flags `-u` and/or `-t`:
```shell
# Use flags to access to repository
python3 -m gitlab2github github -u artem-shestakov -t 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 repo check test_repo
```
