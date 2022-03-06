poetry publish --build --username $USERNAME --password $PASSWORD
# git fetch -p && git branch -vv | awk '/: gone]/{print $1}' | xargs git branch -d