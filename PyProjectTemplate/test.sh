#!/usr/bin/env bash


FEATURE_BRANCH="feature"
HOTFIX_BRANCH="hotfix"
DEVELOP_BRANCH="develop"
MASTER_BRANCH="master"
RELEASE_BRANCH="release"

BASE_NAME=$(basename $0)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd ${DIR}

SERVICES=$@

ALL_SERVICES=$(echo */ | sed "s/\///g")


function change_delimiter() {
    echo $1 | sed "s/$2/$3/g"
}

function contains() {
    [[ $2 =~ (^| )$1($| ) ]]
}

function exit_with_usage() {
    echo "./${BASE_NAME} [$(change_delimiter "${ALL_SERVICES}" " " "|")]"
    exit $1
}

function git_branch_name() {
    git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/\1/'
}


STAGE=$(git_branch_name)
if [[ ${STAGE} == ${FEATURE_BRANCH}* ]]; then
    STAGE="feature"
elif [[ ${STAGE} == ${HOTFIX_BRANCH}* ]]; then
    STAGE="feature"
elif [[ ${STAGE} == ${DEVELOP_BRANCH}* ]]; then
    STAGE="develop"
elif [[ ${STAGE} == ${MASTER_BRANCH}* ]]; then
    STAGE="master"
elif [[ ${STAGE} == ${RELEASE_BRANCH}* ]]; then
    STAGE="master"
else
    echo "Internal error: cannot find the appropriate stage."
fi


export SPIDER_RUNTIME_STAGE=${STAGE}
export SPIDER_RUNTIME_MODE="test"


if [ -z ${SERVICES} ]; then
    SERVICES=${ALL_SERVICES}
fi
for SERVICE in ${SERVICES}; do
    if ! contains "${SERVICE}" "${ALL_SERVICES}"; then
        echo "\"${SERVICE}\" is not a valid service. Available are: ${ALL_SERVICES}."
        exit_with_usage 1
    fi
done


function echo_line() {
    echo
    echo $@
    echo
}

function docker_compose_test() {
    docker-compose -f docker-compose.base.yml \
                   -f docker-compose.${STAGE}.yml \
                   -f docker-compose.test.base.yml \
                   -f docker-compose.test.${STAGE}.yml \
                   $@
}

function set_up() {
    echo_line "Set up test environment."
    docker_compose_test build
    return $?
}

function tear_down() {
    echo_line "Tear down test environment."
    # docker_compose_test stop
    # docker_compose_test rm -f
    docker_compose_test down
}


STOP=0
EXIT_CODE=0
trap "STOP=1" SIGINT SIGKILL SIGTERM

set_up
EXIT_CODE=$?
if [ ${EXIT_CODE} -ne 0 ]; then
    echo_line "Setting up test environment failed."
    STOP=1
fi

for SERVICE in ${SERVICES}; do
    if [ ${STOP} -ne 0 ]; then
        echo_line "Stop the test."
        break
    fi
    echo_line "Run test for \"${SERVICE}\"."
    docker_compose_test run ${SERVICE}
    STATUS_CODE=$?
    if [ ${STATUS_CODE} -ne 0 ]; then
        echo_line "\"${SERVICE}\" fails to pass test."
        EXIT_CODE=${STATUS_CODE}
    fi
done

tear_down

exit ${EXIT_CODE}
