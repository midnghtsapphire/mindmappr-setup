# OpenRouter Team Management Strategy

## Current Team Configuration
- Primary Team: Code Generation
- Secondary Team: Code Review
- Tertiary Team: Specialized Domains

## Deployment Strategy
- Bullpen Rotation
- 15-20 min max per task
- Immediate swap on stall
- Persistent state tracking

## Model Prioritization
1. Code Generation
   - Kimi K2.5 (Primary)
   - DeepSeek V3.2 (Backup)
   - Trinity Large Preview (Fallback)

2. Code Review
   - Venice AI (Primary)
   - Claude Sonnet 4.5 (Secondary)
   - DeepSeek V3.2 Speciale (Fallback)

3. Specialized Domains
   - Gemini 2.5 Pro (Complex Reasoning)
   - Grok 4.1 Fast (Agentic Tasks)
   - Llama 3.3 70B (Free Tier Advanced)

## Skill Download Protocol
- Automated GitHub Cloning
- Accessibility Audit
- Performance Testing
- Integration Verification

## Continuous Improvement
- Track usage per model
- Auto-handoff on rate limiting
- Cost optimization
- Performance benchmarking