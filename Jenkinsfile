pipeline {
    agent any

    stages {
        stage('Build Master') {
            when {
                branch 'master' 
            }
            steps {
                /* Create/Activate  virtualenv */
                python3 -m venv decide-enviroment
                . ./decide-enviroment/bin/activate

                /* Install Requirements */
                pip install -r requirements.txt

                /* Run tests */
                cd decide
                ./manage.py test -v 2
            }
        }

        stage('Deploy Master') {
            when {
                branch 'master' 
            }
            steps {
                /* Llamamos a Heroku y a darle caña */
            }
        }

        stage('Build Develop') {
            when {
                branch 'develop' 
            }
            steps {
                /* Create/Activate  virtualenv */
                python3 -m venv decide-enviroment
                . ./decide-enviroment/bin/activate

                /* Install Requirements */
                pip install -r requirements.txt

                /* Run tests */
                cd decide
                ./manage.py test -v 2
            }
        }

        stage('Build G1') {
            when {
                branch 'G1' 
            }
            steps {
                /* Create/Activate  virtualenv */
                python3 -m venv decide-enviroment
                . ./decide-enviroment/bin/activate

                /* Install Requirements */
                pip install -r requirements.txt

                /* Run tests */
                cd decide
                ./manage.py test -v 2
            }
        }

        stage('Build G2') {
            when {
                branch 'G2' 
            }
            steps {
                /* Create/Activate  virtualenv */
                python3 -m venv decide-enviroment
                . ./decide-enviroment/bin/activate

                /* Install Requirements */
                pip install -r requirements.txt

                /* Run tests */
                cd decide
                ./manage.py test -v 2
            }
        }

        stage('Build G3') {
            when {
                branch 'G3' 
            }
            steps {
                /* Create/Activate  virtualenv */
                python3 -m venv decide-enviroment
                . ./decide-enviroment/bin/activate

                /* Install Requirements */
                pip install -r requirements.txt

                /* Run tests */
                cd decide
                ./manage.py test -v 2
            }
        }
    }
}
