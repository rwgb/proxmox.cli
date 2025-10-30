#!/usr/bin/env bash
# Script to run GitHub Actions locally using act

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if act is installed
if ! command -v act &> /dev/null; then
    echo -e "${RED}Error: act is not installed${NC}"
    echo "Install it with: curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash"
    exit 1
fi

# Function to display usage
usage() {
    echo "Usage: $0 [workflow] [options]"
    echo ""
    echo "Workflows:"
    echo "  tests     - Run the tests workflow (default)"
    echo "  publish   - Run the publish workflow"
    echo "  all       - List all available workflows"
    echo ""
    echo "Options:"
    echo "  --list, -l              - List all jobs in the workflow"
    echo "  --job, -j <job_name>    - Run a specific job"
    echo "  --event, -e <event>     - Specify event type (push, pull_request, release)"
    echo "  --platform <platform>   - Specify platform (ubuntu-latest, macos-latest, windows-latest)"
    echo "  --python <version>      - Test with specific Python version (3.8, 3.9, 3.10, 3.11, 3.12)"
    echo "  --dry-run, -n           - Show what would be run without executing"
    echo "  --verbose, -v           - Verbose output"
    echo "  --help, -h              - Display this help message"
    echo ""
    echo "Examples:"
    echo "  $0 tests                              # Run all test jobs"
    echo "  $0 tests --list                       # List test jobs"
    echo "  $0 tests --python 3.11                # Run tests with Python 3.11 only"
    echo "  $0 tests --job test --platform ubuntu # Run test job on Ubuntu only"
    echo "  $0 publish --event release            # Simulate a release event"
    echo "  $0 all                                # List all workflows"
}

# Default values
WORKFLOW="tests"
EVENT="push"
DRY_RUN=false
LIST_JOBS=false
VERBOSE=""
JOB=""
PLATFORM=""
PYTHON_VERSION=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        tests|publish|all)
            WORKFLOW="$1"
            shift
            ;;
        --list|-l)
            LIST_JOBS=true
            shift
            ;;
        --job|-j)
            JOB="$2"
            shift 2
            ;;
        --event|-e)
            EVENT="$2"
            shift 2
            ;;
        --platform)
            PLATFORM="$2"
            shift 2
            ;;
        --python)
            PYTHON_VERSION="$2"
            shift 2
            ;;
        --dry-run|-n)
            DRY_RUN=true
            shift
            ;;
        --verbose|-v)
            VERBOSE="--verbose"
            shift
            ;;
        --help|-h)
            usage
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            usage
            exit 1
            ;;
    esac
done

# Handle workflow selection
case $WORKFLOW in
    tests)
        WORKFLOW_FILE=".github/workflows/tests.yml"
        ;;
    publish)
        WORKFLOW_FILE=".github/workflows/publish.yml"
        ;;
    all)
        echo -e "${GREEN}Available workflows:${NC}"
        act -l
        exit 0
        ;;
    *)
        echo -e "${RED}Unknown workflow: $WORKFLOW${NC}"
        usage
        exit 1
        ;;
esac

# Check if workflow file exists
if [[ ! -f "$WORKFLOW_FILE" ]]; then
    echo -e "${RED}Error: Workflow file not found: $WORKFLOW_FILE${NC}"
    exit 1
fi

# List jobs if requested
if [[ "$LIST_JOBS" == true ]]; then
    echo -e "${GREEN}Jobs in $WORKFLOW_FILE:${NC}"
    act -l -W "$WORKFLOW_FILE"
    exit 0
fi

# Build act command
ACT_CMD="act"

# Add event type
ACT_CMD="$ACT_CMD $EVENT"

# Add workflow file
ACT_CMD="$ACT_CMD -W $WORKFLOW_FILE"

# Add job if specified
if [[ -n "$JOB" ]]; then
    ACT_CMD="$ACT_CMD -j $JOB"
fi

# Add platform matrix if specified
if [[ -n "$PLATFORM" ]]; then
    ACT_CMD="$ACT_CMD --matrix os:$PLATFORM"
fi

# Add Python version matrix if specified
if [[ -n "$PYTHON_VERSION" ]]; then
    ACT_CMD="$ACT_CMD --matrix python-version:$PYTHON_VERSION"
fi

# Add verbose if requested
if [[ -n "$VERBOSE" ]]; then
    ACT_CMD="$ACT_CMD $VERBOSE"
fi

# Execute or show dry run
if [[ "$DRY_RUN" == true ]]; then
    echo -e "${YELLOW}Dry run - would execute:${NC}"
    echo "$ACT_CMD"
else
    echo -e "${GREEN}Running workflow: $WORKFLOW${NC}"
    echo -e "${YELLOW}Command: $ACT_CMD${NC}"
    echo ""
    eval $ACT_CMD
fi
