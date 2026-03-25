# Jenkins build fails on test

**Data:** 2024-06-14

---

**User:**

I have build.sh where I call python setup.py test where test can fail. build.sh is called from build.gradle
task.register('buildPckg', Exec){
commandLine './build.sh'
doLast {
if (executionResult.get().getExitValue()) {
throw new GradleException("error")
}
}


In Jenkins, gradle is called in that way
script{
sh '''"./gradlew clean build
'''
}

The problem is that when python unit tests fail, the Jenkins build does not fail.

---

**Assistant:**

To ensure that your Jenkins build fails when the Python unit tests fail, you need to ensure that the `build.sh` script correctly returns a non-zero exit code when the tests fail. Additionally, the `build.gradle` script should handle and propagate this failure correctly.

Here's how you can adjust your `build.sh` and `build.gradle` scripts:

### Adjusting `build.sh`
Ensure `build.sh` returns a non-zero exit code if `python setup.py test` fails:

```sh
#!/bin/bash

python setup.py test
test_exit_code=$?

if [ $test_exit_code -ne 0 ]; then
    echo "Python tests failed with exit code $test_exit_code"
    exit $test_exit_code
fi

echo "Python tests passed"
exit 0
```

### Adjusting `build.gradle`
Ensure your `build.gradle` properly handles the exit code from `build.sh`:

```groovy
task register('buildPckg', Exec) {
    commandLine './build.sh'
    doLast {
        if (executionResult.get().getExitValue() != 0) {
            throw new GradleException("Error: Python unit tests failed")
        }
    }
}
```

### Jenkins Pipeline Script
Ensure that the Jenkins pipeline correctly handles the failure:

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                script {
                    sh './gradlew clean build'
                }
            }
        }
    }
    post {
        failure {
            echo "Build failed"
        }
    }
}
```

With these adjustments:

1. `build.sh` will exit with a non-zero status if the Python tests fail.
2. `build.gradle` will catch this non-zero exit status and throw a `GradleException`.
3. Jenkins will then correctly interpret the failure and mark the build as failed.

This setup ensures that any failure in your Python unit tests will propagate through to Jenkins, resulting in a failed build.