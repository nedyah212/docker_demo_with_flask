#!/bin/bash
source .env
JENKINS_URL="$JENKINS_URL"
JENKINS_USER="$JENKINS_USER"
JENKINS_TOKEN="$JENKINS_API_TOKEN"
JENKINSFILE="${1:-Jenkinsfile}"

# Get CSRF crumb (notice "useCrumbs":true in your JSON)
CRUMB=$(curl -s -u "$JENKINS_USER:$JENKINS_TOKEN" \
  "$JENKINS_URL/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,%22:%22,//crumb)")

# Split crumb
CRUMB_FIELD=$(echo $CRUMB | cut -d: -f1)
CRUMB_VALUE=$(echo $CRUMB | cut -d: -f2)

echo "Validating $JENKINSFILE..."
RESULT=$(curl -s -X POST \
  -u "$JENKINS_USER:$JENKINS_TOKEN" \
  -H "$CRUMB_FIELD:$CRUMB_VALUE" \
  -F "jenkinsfile=<$JENKINSFILE" \
  "$JENKINS_URL/pipeline-model-converter/validate")

echo "$RESULT"

if echo "$RESULT" | grep -q "successfully validated"; then
    echo "✓ Jenkinsfile is valid"
    exit 0
else
    echo "✗ Jenkinsfile has errors"
    exit 1
fi
