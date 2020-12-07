# tmux aliases
alias fate='tmux a -t fate'
alias ll='tmux a -t ll'
alias sig='tmux a -t sig'
alias screeninit='tmux new -s'
alias screens='tmux ls'
alias killscreen='tmux kill-ses -t'

# sys aliases
alias pyinit=''
alias ports='sudo lsof -i -P -n | grep LISTEN'
alias venvinit='python3.8 -m venv venv'
alias upgrade='sudo apt upgrade'
alias update='sudo apt update'
alias install='sudo apt-get'