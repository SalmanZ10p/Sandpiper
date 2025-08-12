#!/bin/bash

# Sandpiper Todo API Integration Test Runner
# This script runs comprehensive integration tests for all Todo CRUD endpoints

set -e

# Colors and emojis for better output
CLEAR='\033[0m'
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'

# Emojis for better visual feedback
SUCCESS="✅"
FAILURE="❌"
WARNING="⚠️"
INFO="ℹ️"
ROCKET="🚀"
GEAR="⚙️"
TEST_TUBE="🧪"
CLOCK="⏰"
CHART="📊"
CHECKMARK="✓"
CROSS="✗"

function print_header() {
    echo -e "${CYAN}"
    echo "=================================================================================================="
    echo "🧪 SANDPIPER TODO API INTEGRATION TESTS 🧪"
    echo "=================================================================================================="
    echo -e "${CLEAR}"
    echo -e "${BLUE}${INFO} Test Suite: Todo CRUD Operations${CLEAR}"
    echo -e "${BLUE}${INFO} Date: $(date '+%Y-%m-%d %H:%M:%S')${CLEAR}"
    echo -e "${BLUE}${INFO} Backend URL: http://localhost:5000${CLEAR}"
    echo -e "${GREEN}${INFO} 📧 Email Prevention: Tests use test endpoints to avoid email sending${CLEAR}"
    echo ""
}

function print_step() {
    local step_num=$1
    local step_name=$2
    local description=$3
    
    echo -e "${PURPLE}${GEAR} STEP ${step_num}: ${step_name}${CLEAR}"
    echo -e "${BLUE}   ${description}${CLEAR}"
    echo ""
}

function check_prerequisites() {
    print_step "1" "PREREQUISITES CHECK" "Verifying system requirements and dependencies"
    
    local all_good=true
    
    # Check if Python 3 is available
    if command -v python3 &> /dev/null; then
        local python_version=$(python3 --version 2>&1)
        echo -e "${GREEN}${SUCCESS} Python 3 found: ${python_version}${CLEAR}"
    else
        echo -e "${RED}${FAILURE} Python 3 not found. Please install Python 3.${CLEAR}"
        all_good=false
    fi
    
    # Check if requests library is available
    if python3 -c "import requests" 2>/dev/null; then
        echo -e "${GREEN}${SUCCESS} Python requests library found${CLEAR}"
    else
        echo -e "${YELLOW}${WARNING} Python requests library not found. Installing...${CLEAR}"
        pip3 install requests || {
            echo -e "${RED}${FAILURE} Failed to install requests library${CLEAR}"
            all_good=false
        }
        if [ "$all_good" = true ]; then
            echo -e "${GREEN}${SUCCESS} Python requests library installed successfully${CLEAR}"
        fi
    fi
    
    # Check if the backend is running
    echo -e "${BLUE}${INFO} Checking if Sandpiper backend is running...${CLEAR}"
    if curl -s http://localhost:5000/auth/test > /dev/null 2>&1; then
        echo -e "${GREEN}${SUCCESS} Backend is running and accessible${CLEAR}"
    else
        echo -e "${RED}${FAILURE} Backend is not accessible at http://localhost:5000${CLEAR}"
        echo -e "${YELLOW}${WARNING} Please ensure the backend is running with: ./run.sh${CLEAR}"
        all_good=false
    fi
    
    # Check if integration test file exists
    if [ -f "integration_tests.py" ]; then
        echo -e "${GREEN}${SUCCESS} Integration test file found${CLEAR}"
    else
        echo -e "${RED}${FAILURE} integration_tests.py not found in current directory${CLEAR}"
        all_good=false
    fi
    
    if [ "$all_good" = false ]; then
        echo -e "${RED}${FAILURE} Prerequisites check failed. Please fix the issues above.${CLEAR}"
        exit 1
    fi
    
    echo -e "${GREEN}${SUCCESS} All prerequisites satisfied${CLEAR}"
    echo ""
}

function run_integration_tests() {
    print_step "2" "INTEGRATION TESTS EXECUTION" "Running comprehensive Todo CRUD API tests"
    
    local test_start_time=$(date +%s)
    
    echo -e "${BLUE}${TEST_TUBE} Starting integration tests...${CLEAR}"
    echo ""
    
    # Create logs directory if it doesn't exist
    mkdir -p logs
    
    local log_file="logs/integration_tests_$(date +%Y%m%d_%H%M%S).log"
    
    echo -e "${BLUE}${INFO} Test logs will be saved to: ${log_file}${CLEAR}"
    echo ""
    
    # Run the Python integration tests
    if python3 integration_tests.py 2>&1 | tee "$log_file"; then
        local test_exit_code=${PIPESTATUS[0]}
    else
        local test_exit_code=$?
    fi
    
    local test_end_time=$(date +%s)
    local test_duration=$((test_end_time - test_start_time))
    
    echo ""
    echo -e "${BLUE}${CLOCK} Test execution completed in ${test_duration} seconds${CLEAR}"
    
    return $test_exit_code
}

function analyze_test_results() {
    print_step "3" "RESULTS ANALYSIS" "Analyzing test results and generating summary"
    
    local log_file=$(ls -t logs/integration_tests_*.log 2>/dev/null | head -n1)
    
    if [ -z "$log_file" ]; then
        echo -e "${YELLOW}${WARNING} No log file found for analysis${CLEAR}"
        return 1
    fi
    
    echo -e "${BLUE}${INFO} Analyzing results from: ${log_file}${CLEAR}"
    echo ""
    
    # Count test results
    local passed_tests=$(grep -c "✅ PASSED:" "$log_file" 2>/dev/null || echo "0")
    local failed_tests=$(grep -c "❌ FAILED:" "$log_file" 2>/dev/null || echo "0")
    local total_tests=$((passed_tests + failed_tests))
    
    # Calculate success rate
    local success_rate=0
    if [ $total_tests -gt 0 ]; then
        success_rate=$(echo "scale=1; $passed_tests * 100 / $total_tests" | bc -l 2>/dev/null || echo "0")
    fi
    
    echo -e "${CYAN}${CHART} TEST RESULTS SUMMARY:${CLEAR}"
    echo -e "${GREEN}   ${SUCCESS} Passed Tests: ${passed_tests}${CLEAR}"
    echo -e "${RED}   ${FAILURE} Failed Tests: ${failed_tests}${CLEAR}"
    echo -e "${BLUE}   ${INFO} Total Tests: ${total_tests}${CLEAR}"
    echo -e "${PURPLE}   ${CHART} Success Rate: ${success_rate}%${CLEAR}"
    echo ""
    
    # Show failed tests if any
    if [ $failed_tests -gt 0 ]; then
        echo -e "${RED}${FAILURE} FAILED TEST DETAILS:${CLEAR}"
        grep "❌ FAILED:" "$log_file" | while read -r line; do
            echo -e "${RED}   $line${CLEAR}"
        done
        echo ""
    fi
    
    # Check for specific test types
    echo -e "${BLUE}${INFO} CRUD OPERATION BREAKDOWN:${CLEAR}"
    
    local create_test=$(grep -c "Create Todo.*✅ PASSED" "$log_file" 2>/dev/null || echo "0")
    local read_test=$(grep -c "Read Todos.*✅ PASSED" "$log_file" 2>/dev/null || echo "0")
    local update_test=$(grep -c "Update Todo.*✅ PASSED" "$log_file" 2>/dev/null || echo "0")
    local delete_test=$(grep -c "Delete Todo.*✅ PASSED" "$log_file" 2>/dev/null || echo "0")
    
    echo -e "   📝 Create Todo Test: $( [ $create_test -gt 0 ] && echo -e "${GREEN}${CHECKMARK} PASSED${CLEAR}" || echo -e "${RED}${CROSS} FAILED${CLEAR}" )"
    echo -e "   📖 Read Todos Test:  $( [ $read_test -gt 0 ] && echo -e "${GREEN}${CHECKMARK} PASSED${CLEAR}" || echo -e "${RED}${CROSS} FAILED${CLEAR}" )"
    echo -e "   ✏️  Update Todo Test: $( [ $update_test -gt 0 ] && echo -e "${GREEN}${CHECKMARK} PASSED${CLEAR}" || echo -e "${RED}${CROSS} FAILED${CLEAR}" )"
    echo -e "   🗑️  Delete Todo Test: $( [ $delete_test -gt 0 ] && echo -e "${GREEN}${CHECKMARK} PASSED${CLEAR}" || echo -e "${RED}${CROSS} FAILED${CLEAR}" )"
    echo ""
    
    return $failed_tests
}

function print_recommendations() {
    local failed_count=$1
    
    print_step "4" "RECOMMENDATIONS" "Providing next steps based on test results"
    
    if [ $failed_count -eq 0 ]; then
        echo -e "${GREEN}${SUCCESS} All tests passed! Your Todo API is working correctly.${CLEAR}"
        echo -e "${BLUE}${INFO} Recommendations:${CLEAR}"
        echo -e "   • Consider adding more edge case tests"
        echo -e "   • Run tests regularly during development"
        echo -e "   • Consider adding performance tests"
        echo -e "   • Add these tests to your CI/CD pipeline"
    else
        echo -e "${RED}${FAILURE} Some tests failed. Please review the issues above.${CLEAR}"
        echo -e "${BLUE}${INFO} Recommended actions:${CLEAR}"
        echo -e "   • Check the detailed error messages in the log file"
        echo -e "   • Verify your API endpoints are working correctly"
        echo -e "   • Check database connectivity and data integrity"
        echo -e "   • Review the authentication flow"
        echo -e "   • Consider running individual tests for debugging"
    fi
    echo ""
}

function cleanup() {
    print_step "5" "CLEANUP" "Cleaning up test artifacts"
    
    echo -e "${BLUE}${INFO} Test run completed${CLEAR}"
    echo -e "${BLUE}${INFO} Log files are preserved in the logs/ directory${CLEAR}"
    echo ""
}

function print_footer() {
    local exit_code=$1
    
    echo -e "${CYAN}"
    echo "=================================================================================================="
    
    if [ $exit_code -eq 0 ]; then
        echo -e "${GREEN}${SUCCESS} INTEGRATION TESTS COMPLETED SUCCESSFULLY ${SUCCESS}${CLEAR}"
    else
        echo -e "${RED}${FAILURE} INTEGRATION TESTS COMPLETED WITH FAILURES ${FAILURE}${CLEAR}"
    fi
    
    echo -e "${CYAN}=================================================================================================="
    echo -e "${CLEAR}"
    echo -e "${BLUE}${CLOCK} Finished at: $(date '+%Y-%m-%d %H:%M:%S')${CLEAR}"
    echo ""
}

function show_help() {
    echo "Sandpiper Todo API Integration Test Runner"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "OPTIONS:"
    echo "  -h, --help     Show this help message"
    echo "  -v, --verbose  Enable verbose output"
    echo ""
    echo "DESCRIPTION:"
    echo "  This script runs comprehensive integration tests for the Sandpiper Todo API."
    echo "  It tests all CRUD operations (Create, Read, Update, Delete) for todo items."
    echo ""
    echo "PREREQUISITES:"
    echo "  • Python 3 with requests library"
    echo "  • Sandpiper backend running on localhost:5000"
    echo "  • Database properly initialized"
    echo ""
    echo "TEST COVERAGE:"
    echo "  • Create Todo: Test creating todos with various data"
    echo "  • Read Todos: Test retrieving todos with filters (all, active, completed)"
    echo "  • Update Todo: Test updating todo properties and completion status"
    echo "  • Delete Todo: Test deleting todos and verifying removal"
    echo ""
    echo "EMAIL PREVENTION:"
    echo "  • Tests use /test/create_user endpoint to avoid email sending"
    echo "  • Prevents failed deliveries to test email addresses"
    echo "  • Protects MailJet account deliverability metrics"
    echo ""
    echo "OUTPUT:"
    echo "  • Real-time progress with emojis and colors"
    echo "  • Detailed logs saved to logs/ directory"
    echo "  • Summary with success rate and recommendations"
    echo ""
}

# Main execution
function main() {
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -v|--verbose)
                set -x
                shift
                ;;
            *)
                echo -e "${RED}${FAILURE} Unknown option: $1${CLEAR}"
                echo "Use -h or --help for usage information"
                exit 1
                ;;
        esac
    done
    
    # Store script start time
    local script_start_time=$(date +%s)
    
    # Print header
    print_header
    
    # Main execution flow
    local exit_code=0
    
    # Step 1: Check prerequisites
    check_prerequisites || exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        # Step 2: Run integration tests
        run_integration_tests
        exit_code=$?
        
        # Step 3: Analyze results
        analyze_test_results
        local failed_count=$?
        
        # Update exit code based on test results
        if [ $failed_count -gt 0 ]; then
            exit_code=1
        fi
        
        # Step 4: Print recommendations
        print_recommendations $failed_count
        
        # Step 5: Cleanup
        cleanup
    fi
    
    # Calculate total execution time
    local script_end_time=$(date +%s)
    local total_duration=$((script_end_time - script_start_time))
    echo -e "${BLUE}${CLOCK} Total execution time: ${total_duration} seconds${CLEAR}"
    
    # Print footer
    print_footer $exit_code
    
    exit $exit_code
}

# Check if script is being run directly (not sourced)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
