#!/bin/bash
# =============================================================================
# MindMappr Job Queue System
# =============================================================================
# A cron-based job queue that allows assigning tasks to MindMappr (OpenClaw)
# for overnight/autonomous execution.
#
# Usage:
#   mindmappr-queue add <category> "task description"
#   mindmappr-queue list
#   mindmappr-queue status
#   mindmappr-queue run
#   mindmappr-queue log [job_id]
#   mindmappr-queue clear-completed
#
# Categories: seo, social, scraping, monitoring, docs, research
# =============================================================================

QUEUE_DIR="/opt/mindmappr-queue"
JOBS_DIR="$QUEUE_DIR/jobs"
LOGS_DIR="$QUEUE_DIR/logs"
RESULTS_DIR="$QUEUE_DIR/results"
LOCK_FILE="$QUEUE_DIR/.lock"
OPENCLAW_CMD="/opt/openclaw/dist/index.js"

# Ensure directories exist
mkdir -p "$JOBS_DIR" "$LOGS_DIR" "$RESULTS_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Generate job ID
generate_id() {
    date +%Y%m%d%H%M%S-$(head -c 4 /dev/urandom | xxd -p)
}

# Add a job to the queue
cmd_add() {
    local category="$1"
    local description="$2"
    local priority="${3:-normal}"

    if [ -z "$category" ] || [ -z "$description" ]; then
        echo -e "${RED}Usage: mindmappr-queue add <category> \"description\" [priority]${NC}"
        echo "Categories: seo, social, scraping, monitoring, docs, research"
        echo "Priorities: low, normal, high, critical"
        return 1
    fi

    # Validate category
    case "$category" in
        seo|social|scraping|monitoring|docs|research) ;;
        *)
            echo -e "${RED}Invalid category: $category${NC}"
            echo "Valid categories: seo, social, scraping, monitoring, docs, research"
            return 1
            ;;
    esac

    local job_id=$(generate_id)
    local job_file="$JOBS_DIR/$job_id.json"

    cat > "$job_file" << EOF
{
    "id": "$job_id",
    "category": "$category",
    "description": "$description",
    "priority": "$priority",
    "status": "queued",
    "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "started_at": null,
    "completed_at": null,
    "result": null,
    "error": null,
    "retries": 0,
    "max_retries": 3
}
EOF

    echo -e "${GREEN}Job added: $job_id${NC}"
    echo -e "  Category: ${CYAN}$category${NC}"
    echo -e "  Priority: ${YELLOW}$priority${NC}"
    echo -e "  Description: $description"
}

# List all jobs
cmd_list() {
    echo -e "${BLUE}=== MindMappr Job Queue ===${NC}"
    echo ""

    local count=0
    for job_file in "$JOBS_DIR"/*.json; do
        [ -f "$job_file" ] || continue
        count=$((count + 1))

        local id=$(python3 -c "import json; print(json.load(open('$job_file'))['id'])")
        local cat=$(python3 -c "import json; print(json.load(open('$job_file'))['category'])")
        local desc=$(python3 -c "import json; print(json.load(open('$job_file'))['description'])")
        local status=$(python3 -c "import json; print(json.load(open('$job_file'))['status'])")
        local priority=$(python3 -c "import json; print(json.load(open('$job_file'))['priority'])")
        local created=$(python3 -c "import json; print(json.load(open('$job_file'))['created_at'])")

        # Color-code status
        case "$status" in
            queued) status_color="${YELLOW}QUEUED${NC}" ;;
            running) status_color="${BLUE}RUNNING${NC}" ;;
            completed) status_color="${GREEN}COMPLETED${NC}" ;;
            failed) status_color="${RED}FAILED${NC}" ;;
            *) status_color="$status" ;;
        esac

        echo -e "  [$status_color] ${CYAN}$id${NC}"
        echo -e "    Category: $cat | Priority: $priority | Created: $created"
        echo -e "    $desc"
        echo ""
    done

    if [ $count -eq 0 ]; then
        echo -e "  ${YELLOW}No jobs in queue.${NC}"
    else
        echo -e "  ${GREEN}Total: $count jobs${NC}"
    fi
}

# Show queue status
cmd_status() {
    echo -e "${BLUE}=== Queue Status ===${NC}"

    local queued=0 running=0 completed=0 failed=0
    for job_file in "$JOBS_DIR"/*.json; do
        [ -f "$job_file" ] || continue
        local status=$(python3 -c "import json; print(json.load(open('$job_file'))['status'])")
        case "$status" in
            queued) queued=$((queued + 1)) ;;
            running) running=$((running + 1)) ;;
            completed) completed=$((completed + 1)) ;;
            failed) failed=$((failed + 1)) ;;
        esac
    done

    echo -e "  ${YELLOW}Queued:${NC}    $queued"
    echo -e "  ${BLUE}Running:${NC}   $running"
    echo -e "  ${GREEN}Completed:${NC} $completed"
    echo -e "  ${RED}Failed:${NC}    $failed"
    echo ""

    # Check if cron is set up
    if crontab -l 2>/dev/null | grep -q "mindmappr-queue"; then
        echo -e "  ${GREEN}Cron: Active${NC}"
    else
        echo -e "  ${YELLOW}Cron: Not configured (run 'mindmappr-queue install-cron')${NC}"
    fi

    # Check OpenClaw status
    if systemctl is-active --quiet openclaw; then
        echo -e "  ${GREEN}OpenClaw: Running${NC}"
    else
        echo -e "  ${RED}OpenClaw: Stopped${NC}"
    fi
}

# Build the prompt for OpenClaw based on job category
build_prompt() {
    local category="$1"
    local description="$2"

    case "$category" in
        seo)
            echo "You are working on an SEO content generation task. Generate high-quality, SEO-optimized content based on the following request. Include relevant keywords, meta descriptions, and structured content. Task: $description"
            ;;
        social)
            echo "You are working on social media content creation. Create engaging social media posts optimized for multiple platforms (Instagram, TikTok, LinkedIn, Facebook). Include hashtags, hooks, and call-to-actions. Task: $description"
            ;;
        scraping)
            echo "You are working on a public records research task for insurance leads. Search publicly available data sources, compile findings into a structured format with contact information where available. Task: $description"
            ;;
        monitoring)
            echo "You are performing app monitoring and uptime checks. Check the status of services, verify endpoints are responding, and report any issues found. Task: $description"
            ;;
        docs)
            echo "You are generating documentation. Create comprehensive, well-structured documentation based on the following request. Use markdown format with clear headings, examples, and explanations. Task: $description"
            ;;
        research)
            echo "You are conducting a research task. Gather information from available sources, analyze findings, and produce a comprehensive research report with citations and recommendations. Task: $description"
            ;;
    esac
}

# Run the next queued job
cmd_run() {
    # Check lock
    if [ -f "$LOCK_FILE" ]; then
        local lock_pid=$(cat "$LOCK_FILE")
        if kill -0 "$lock_pid" 2>/dev/null; then
            echo -e "${YELLOW}Queue runner already active (PID: $lock_pid)${NC}"
            return 0
        else
            rm -f "$LOCK_FILE"
        fi
    fi

    echo $$ > "$LOCK_FILE"
    trap "rm -f $LOCK_FILE" EXIT

    # Find next job (priority order: critical > high > normal > low)
    local next_job=""
    for priority in critical high normal low; do
        for job_file in "$JOBS_DIR"/*.json; do
            [ -f "$job_file" ] || continue
            local status=$(python3 -c "import json; print(json.load(open('$job_file'))['status'])")
            local job_priority=$(python3 -c "import json; print(json.load(open('$job_file'))['priority'])")
            if [ "$status" = "queued" ] && [ "$job_priority" = "$priority" ]; then
                next_job="$job_file"
                break 2
            fi
        done
    done

    if [ -z "$next_job" ]; then
        echo -e "${GREEN}No queued jobs to run.${NC}"
        return 0
    fi

    local job_id=$(python3 -c "import json; print(json.load(open('$next_job'))['id'])")
    local category=$(python3 -c "import json; print(json.load(open('$next_job'))['category'])")
    local description=$(python3 -c "import json; print(json.load(open('$next_job'))['description'])")

    echo -e "${BLUE}Running job: $job_id ($category)${NC}"

    # Update status to running
    python3 -c "
import json
with open('$next_job') as f:
    job = json.load(f)
job['status'] = 'running'
job['started_at'] = '$(date -u +%Y-%m-%dT%H:%M:%SZ)'
with open('$next_job', 'w') as f:
    json.dump(job, f, indent=2)
"

    # Build the prompt and send to OpenClaw via gateway API
    local prompt=$(build_prompt "$category" "$description")
    local log_file="$LOGS_DIR/$job_id.log"
    local result_file="$RESULTS_DIR/$job_id.md"

    echo "Job: $job_id" > "$log_file"
    echo "Category: $category" >> "$log_file"
    echo "Started: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$log_file"
    echo "Prompt: $prompt" >> "$log_file"
    echo "---" >> "$log_file"

    # Send to OpenClaw gateway
    local response=$(curl -s -X POST "http://127.0.0.1:18789/api/v1/chat" \
        -H "Authorization: Bearer 687d8749e15c33a21161065852e89d02631ddf63b9505bf32c24adca5acc248d" \
        -H "Content-Type: application/json" \
        -d "{\"message\": \"$prompt\"}" \
        --max-time 300 2>&1)

    local exit_code=$?

    if [ $exit_code -eq 0 ] && echo "$response" | python3 -c "import sys,json; json.load(sys.stdin)" 2>/dev/null; then
        # Extract response text
        local result_text=$(echo "$response" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if isinstance(data, dict):
    print(data.get('response', data.get('message', data.get('text', json.dumps(data)))))
else:
    print(str(data))
" 2>/dev/null)

        echo "$result_text" > "$result_file"
        echo "Response saved to: $result_file" >> "$log_file"

        # Update job status to completed
        python3 -c "
import json
with open('$next_job') as f:
    job = json.load(f)
job['status'] = 'completed'
job['completed_at'] = '$(date -u +%Y-%m-%dT%H:%M:%SZ)'
job['result'] = '$result_file'
with open('$next_job', 'w') as f:
    json.dump(job, f, indent=2)
"
        echo -e "${GREEN}Job $job_id completed.${NC}"
    else
        echo "ERROR: $response" >> "$log_file"

        # Update job status
        python3 -c "
import json
with open('$next_job') as f:
    job = json.load(f)
job['retries'] = job.get('retries', 0) + 1
if job['retries'] >= job.get('max_retries', 3):
    job['status'] = 'failed'
    job['error'] = 'Max retries exceeded'
else:
    job['status'] = 'queued'
job['completed_at'] = '$(date -u +%Y-%m-%dT%H:%M:%SZ)'
with open('$next_job', 'w') as f:
    json.dump(job, f, indent=2)
"
        echo -e "${RED}Job $job_id failed. Check log: $log_file${NC}"
    fi
}

# Run all queued jobs sequentially
cmd_run_all() {
    echo -e "${BLUE}=== Running all queued jobs ===${NC}"
    local count=0
    while true; do
        local has_queued=false
        for job_file in "$JOBS_DIR"/*.json; do
            [ -f "$job_file" ] || continue
            local status=$(python3 -c "import json; print(json.load(open('$job_file'))['status'])")
            if [ "$status" = "queued" ]; then
                has_queued=true
                break
            fi
        done

        if [ "$has_queued" = false ]; then
            break
        fi

        cmd_run
        count=$((count + 1))
        sleep 5  # Brief pause between jobs
    done

    echo -e "${GREEN}Processed $count jobs.${NC}"
}

# View job log
cmd_log() {
    local job_id="$1"
    if [ -z "$job_id" ]; then
        echo -e "${BLUE}=== Recent Logs ===${NC}"
        ls -lt "$LOGS_DIR"/*.log 2>/dev/null | head -10
        return
    fi

    local log_file="$LOGS_DIR/$job_id.log"
    if [ -f "$log_file" ]; then
        cat "$log_file"
    else
        echo -e "${RED}No log found for job: $job_id${NC}"
    fi
}

# Clear completed jobs
cmd_clear() {
    local count=0
    for job_file in "$JOBS_DIR"/*.json; do
        [ -f "$job_file" ] || continue
        local status=$(python3 -c "import json; print(json.load(open('$job_file'))['status'])")
        if [ "$status" = "completed" ]; then
            rm -f "$job_file"
            count=$((count + 1))
        fi
    done
    echo -e "${GREEN}Cleared $count completed jobs.${NC}"
}

# Install cron jobs
cmd_install_cron() {
    # Remove existing mindmappr-queue entries
    crontab -l 2>/dev/null | grep -v "mindmappr-queue" > /tmp/crontab.tmp

    # Add new cron entries
    cat >> /tmp/crontab.tmp << 'CRON'
# MindMappr Job Queue - Process jobs every 30 minutes overnight (10 PM - 6 AM)
0,30 22-23,0-5 * * * /usr/local/bin/mindmappr-queue run-all >> /opt/mindmappr-queue/logs/cron.log 2>&1
# MindMappr Job Queue - Process high-priority jobs every 15 minutes during the day
*/15 6-21 * * * /usr/local/bin/mindmappr-queue run >> /opt/mindmappr-queue/logs/cron.log 2>&1
# MindMappr Job Queue - Daily status report at 6 AM
0 6 * * * /usr/local/bin/mindmappr-queue status >> /opt/mindmappr-queue/logs/daily-report.log 2>&1
CRON

    crontab /tmp/crontab.tmp
    rm -f /tmp/crontab.tmp
    echo -e "${GREEN}Cron jobs installed:${NC}"
    echo "  - Overnight batch processing (10 PM - 6 AM, every 30 min)"
    echo "  - Daytime high-priority processing (every 15 min)"
    echo "  - Daily status report (6 AM)"
}

# Main command router
case "${1:-help}" in
    add)        cmd_add "$2" "$3" "$4" ;;
    list)       cmd_list ;;
    status)     cmd_status ;;
    run)        cmd_run ;;
    run-all)    cmd_run_all ;;
    log)        cmd_log "$2" ;;
    clear)      cmd_clear ;;
    install-cron) cmd_install_cron ;;
    help|*)
        echo -e "${BLUE}MindMappr Job Queue${NC}"
        echo ""
        echo "Usage: mindmappr-queue <command> [args]"
        echo ""
        echo "Commands:"
        echo "  add <category> \"description\" [priority]  Add a job to the queue"
        echo "  list                                      List all jobs"
        echo "  status                                    Show queue status"
        echo "  run                                       Run the next queued job"
        echo "  run-all                                   Run all queued jobs"
        echo "  log [job_id]                              View job logs"
        echo "  clear                                     Clear completed jobs"
        echo "  install-cron                              Install cron schedule"
        echo ""
        echo "Categories: seo, social, scraping, monitoring, docs, research"
        echo "Priorities: low, normal, high, critical"
        ;;
esac
