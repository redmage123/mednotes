#!/bin/bash

# Define Variables
PROJECT_ROOT="/home/bbrelin/src/repos/mednotes"
MINIKUBE_LOCATION="/usr/local/bin/minikube"
TERRAFORM_LOCATION="/usr/local/bin/terraform"
DOCKER_LOCATION="/usr/bin/docker"
TERRAFORM_ROOT="${PROJECT_ROOT}/terraform"

# Function to start the application
start_app() {
  # Start minikube
  if pgrep minikube > /dev/null; then
    echo "Minikube is already running"
  else
    ${MINIKUBE_LOCATION} start
  fi  

  # Start Docker
  sudo systemctl start docker 

  # Apply Terraform
  pushd ${TERRAFORM_ROOT} > /dev/null
  terraform apply ${TERRAFORM_ROOT}/mednotes.plan
  if [ $? -ne 0 ]; then
    terraform init
    terraform plan --out mednotes.plan
    terraform apply mednotes.plan
    if [ $? -ne 0 ]; then
      echo "Error applying Terraform. Exiting."
      exit 1
    fi  
  fi
  popd > /dev/null
}

# Function to stop the application
stop_app() {
  # Stop minikube
  if pgrep minikube > /dev/null; then
    ${MINIKUBE_LOCATION} stop
  else
    echo "Minikube is not running"
  fi    # Stop Docker
  sudo systemctl stop  docker 

  # Destroy Terraform
  pushd ${TERRAFORM_ROOT} > /dev/null
  terraform destroy

  popd > /dev/null
}

# Function to get the status of the application
status_app() {
  echo "Minikube Status:"
  if pgrep minikube > /dev/null; then
    echo "Running"
  else
    echo "Stopped"
  fi

  echo "Docker Status:"
  sudo service docker status
}

# Main Function
main() {
    if [ $# -eq 0 ]; then
        echo "No argument passed. Please pass 'start', 'stop', or 'status'"
        exit 1
    fi
    case $1 in
        "start") 
            start_app
	    ;;
        "stop")
            stop_app
	    ;;
        "status")
            status_app
	    ;;
        *)
            echo "Invalid argument. Please pass 'start', 'stop', or 'status'"
            exit 1
    esac
}
main "$@"

