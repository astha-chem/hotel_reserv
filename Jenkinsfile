pipeline{
    agent any

    environment {
        VENV_DIR = 'myvenv'
        GCP_PROJECT= 'mlops-468305'
        GCLOUD_PATH = '/var/jenkins_home/google-cloud-sdk/bin'
        DOCKER_CLI_EXPERIMENTAL='enabled'
    }

    stages{
        stage('Cloning Github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins....'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/astha-chem/hotel_reserv.git']])
                }
            }
        }

        stage('Set up Docker Buildx') {
            steps {
                script{
                    echo 'Setting up Docker Buildx...'
                    sh ''' 
                    # Make sure buildx is available
                    docker buildx version || true

                    # Create a builder if not already there
                    docker buildx create --name mybuilder --use || docker buildx use mybuilder
                    docker buildx inspect --bootstrap
                    '''
                }
            }
        }

        stage('Setting up venv and installing dependencies'){
            steps{
                script{
                    echo 'Setting up venv and installing dependencies....'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }

        stage('Building and pushing docker image to GCR'){
            steps{
                withCredentials([file(credentialsId : 'gcp-key', variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Building and pushing docker image to GCR .......'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet 
                        docker buildx build --platform linux/amd64 \
                        -t gcr.io/${GCP_PROJECT}/hotel-reserv:latest \
                        --push .
                        '''
                    }
                }
            }
        }

        stage('Deploy to Google Cloud Run'){
            steps{
                withCredentials([file(credentialsId: 'gcp-key' , variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Deploy to Google Cloud Run.............'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}

                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud run deploy hotel-reserv \
                            --image=gcr.io/${GCP_PROJECT}/hotel-reserv:latest \
                            --platform=managed \
                            --region=us-central1 \
                            --allow-unauthenticated
                            --timeout=10m
                        '''
                    }
                }
            }
        }
    }
}