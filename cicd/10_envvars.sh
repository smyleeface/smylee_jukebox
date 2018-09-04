#!/usr/bin/env bash

set -e

echo "AWS_DEFAULT_REGION ${AWS_DEFAULT_REGION}"
echo "AWS_REGION ${AWS_REGION}"
echo "CODEBUILD_BUILD_ARN ${CODEBUILD_BUILD_ARN}"
echo "CODEBUILD_BUILD_ID ${CODEBUILD_BUILD_ID}"
echo "CODEBUILD_BUILD_IMAGE ${CODEBUILD_BUILD_IMAGE}"
echo "CODEBUILD_BUILD_SUCCEEDING ${CODEBUILD_BUILD_SUCCEEDING}"
echo "CODEBUILD_INITIATOR ${CODEBUILD_INITIATOR}"
echo "CODEBUILD_KMS_KEY_ID ${CODEBUILD_KMS_KEY_ID}"
echo "CODEBUILD_LOG_PATH ${CODEBUILD_LOG_PATH}"
echo "CODEBUILD_RESOLVED_SOURCE_VERSION ${CODEBUILD_RESOLVED_SOURCE_VERSION}"
echo "CODEBUILD_SOURCE_REPO_URL ${CODEBUILD_SOURCE_REPO_URL}"
echo "CODEBUILD_SOURCE_VERSION ${CODEBUILD_SOURCE_VERSION}"
echo "CODEBUILD_SRC_DIR ${CODEBUILD_SRC_DIR}"
echo "CODEBUILD_START_TIME ${CODEBUILD_START_TIME}"
echo "HOME ${HOME}"

export GITSHA=$(git log -1 --format="%H")
echo "GITSHA ${GITSHA}"

# TODO: git branch lookup is not accurate, might need a different setup to report results
# -- write results to s3 and trigger lambda to send? -- then any project can use s3 bucket to send
export GIT_BRANCH=$(git branch --contains ${GITSHA} | sed -n '2 p' | sed -e 's/^*//')
echo "GIT_BRANCH ${GIT_BRANCH}"

export GIT_AUTHOR_EMAIL=$(git log -1 --format="%aE")
echo "GIT_AUTHOR_EMAIL ${GIT_AUTHOR_EMAIL}"

export GIT_AUTHOR_NAME=$(git log -1 --format="%aN")
echo "GIT_AUTHOR_NAME ${GIT_AUTHOR_NAME}"

export GIT_COMMIT_MESSAGE=$(git log -1 --format="%B")
echo "GIT_COMMIT_MESSAGE ${GIT_COMMIT_MESSAGE}"