# Agent Evaluation Guide: Structured Output Patterns for Quality Assurance

## Table of Contents
1. [Introduction](#introduction)
2. [Core Principles](#core-principles)
3. [Evaluation Type Matrix](#evaluation-type-matrix)
4. [Detailed Evaluation Patterns](#detailed-evaluation-patterns)
5. [Implementation Examples](#implementation-examples)
6. [Integration Patterns](#integration-patterns)
7. [Domain-Specific Applications](#domain-specific-applications)
8. [Best Practices](#best-practices)
9. [Common Pitfalls](#common-pitfalls)
10. [Quick Reference](#quick-reference)

## Introduction

This guide provides comprehensive patterns for implementing evaluation systems in AI agent architectures using structured JSON outputs. All patterns are designed for use with OpenAI Agents SDK, LiteLLM, and OpenRouter (specifically Gemini 2.5 Flash).

### Why Structured Output Evaluation?

Traditional LLM outputs can be unpredictable and difficult to parse programmatically. By using structured JSON outputs with defined schemas, we achieve:

- **Deterministic decision flow**: Boolean fields drive workflow branches
- **Granular feedback**: Structured data enables targeted improvements
- **Programmatic integration**: JSON parsing eliminates regex/string manipulation
- **Audit trails**: Complete evaluation reasoning captured in structured format
- **Consistency**: Temperature=0.2 ensures reliable evaluation behavior

## Core Principles

### 1. Every Evaluation Returns JSON

All evaluation agents must use `response_format={"type": "json_object"}` and include clear instructions about the expected JSON structure.

### 2. Decision Fields Drive Workflow

Each evaluation type includes a primary decision field (`pass`, `acceptable`, `proceed`, etc.) that determines the next workflow step.

### 3. Feedback Enables Improvement

Evaluations should provide actionable feedback that can be fed back to generation agents for improvement loops.

### 4. Temperature = 0.2

Lower temperature ensures consistent evaluation behavior across runs.

## Evaluation Type Matrix

### Decision Tree for Evaluation Selection

```python
def select_evaluation_type(context):
    """Select appropriate evaluation pattern based on workflow needs"""
    
    # Question 1: Is this a binary gate or quality gradient?
    if context.has_clear_pass_fail_criteria and not context.needs_quality_feedback:
        return "BinaryGate"
    
    # Question 2: Are we comparing before/after states?
    if context.has_original_and_revised_versions:
        return "DifferentialEvaluation"
    
    # Question 3: Do we have a fixed checklist of requirements?
    if context.has_explicit_requirements_list:
        return "ComplianceCheck"
    
    # Question 4: Do issues have different severity levels?
    if context.issues_have_blocking_vs_warning_levels:
        return "CriticalityAssessment"
    
    # Question 5: Default - multi-dimensional quality assessment
    return "RubricScoring"
```

### Quick Reference Table

| Question | Evaluation Type | Primary Use Case |
|----------|----------------|------------------|
| Can we proceed? | BinaryGate | Security checks, format validation |
| How good is this? | RubricScoring | Content quality, code review |
| Did we improve? | DifferentialEvaluation | Edit verification, optimization |
| Are we compliant? | ComplianceCheck | Regulatory, API contracts |
| What must we fix? | CriticalityAssessment | Bug triage, production readiness |

## Detailed Evaluation Patterns

### 1. BinaryGate

**Purpose**: Simple pass/fail decisions with clear thresholds

**When to Use**:
- Single go/no-go decision needed
- Clear pass/fail criteria exist
- No quality gradient needed
- Boolean workflow branching

**JSON Schema**:
```json
{
    "pass": boolean,
    "reason": string,
    "details": string (optional)
}
```

**Example Scenarios**:
- Security clearance (contains PII?)
- Format validation (valid JSON?)
- Prerequisite check (dependencies met?)
- Access control (user authorized?)

### 2. RubricScoring

**Purpose**: Multi-dimensional quality assessment with scores

**When to Use**:
- Multiple quality aspects to evaluate
- Gradual improvement possible
- Need diagnostic feedback for retry
- Quality thresholds for acceptance

**JSON Schema**:
```json
{
    "dimensions": {
        "dimension_1": {
            "score": integer (1-5),
            "note": string,
            "weight": number (optional)
        },
        "dimension_2": {...}
    },
    "overall_score": number,
    "acceptable": boolean,
    "improvement_priority": string,
    "strengths": [string],
    "weaknesses": [string]
}
```

**Example Scenarios**:
- Content quality (clarity, accuracy, completeness)
- Code review (style, performance, security)
- Documentation (coverage, clarity, examples)
- UI/UX review (usability, aesthetics, accessibility)

### 3. DifferentialEvaluation

**Purpose**: Compare before/after states to verify improvements

**When to Use**:
- Comparing original vs revised versions
- Measuring improvement/regression
- Validating that changes preserve good qualities
- A/B testing scenarios

**JSON Schema**:
```json
{
    "improved": boolean,
    "preserved_strengths": boolean,
    "new_issues": [
        {
            "issue": string,
            "severity": string
        }
    ],
    "fixed_issues": [string],
    "net_better": boolean,
    "improvement_score": number (-1 to 1),
    "recommendation": string
}
```

**Example Scenarios**:
- Edit verification (writing improvements)
- Optimization validation (performance tuning)
- Refactoring assessment (code cleanup)
- Translation quality (preserving meaning)

### 4. ComplianceCheck

**Purpose**: Verify adherence to fixed requirements/standards

**When to Use**:
- Fixed requirements list exists
- Binary compliance per requirement
- Audit trail needed
- Regulatory/contractual obligations

**JSON Schema**:
```json
{
    "requirements": {
        "req_id_1": {
            "met": boolean,
            "evidence": string,
            "notes": string (optional)
        },
        "req_id_2": {...}
    },
    "fully_compliant": boolean,
    "compliance_percentage": number,
    "missing_requirements": [string],
    "critical_failures": [string]
}
```

**Example Scenarios**:
- Regulatory compliance (GDPR, HIPAA)
- API contract validation
- Style guide adherence
- Security standards (OWASP)

### 5. CriticalityAssessment

**Purpose**: Triage issues by severity with prioritization

**When to Use**:
- Issues have different severity levels
- Some problems block, others are warnings
- Need triage/prioritization
- Resource allocation decisions

**JSON Schema**:
```json
{
    "blockers": [
        {
            "issue": string,
            "component": string,
            "fix_required": string,
            "estimated_effort": string (optional)
        }
    ],
    "warnings": [
        {
            "issue": string,
            "suggestion": string,
            "impact": string (optional)
        }
    ],
    "info": [string],
    "proceed": boolean,
    "priority_fix": string,
    "risk_level": string ("low"|"medium"|"high"|"critical")
}
```

**Example Scenarios**:
- Security vulnerability assessment
- Production readiness review
- Data quality validation
- Performance bottleneck analysis

## Implementation Examples

### Complete Binary Gate Implementation

```python
from agents import Agent, Runner
from agents.extensions.models.litellm_model import LitellmModel
import json

# Configure model
model = LitellmModel(
    model="openrouter/google/gemini-2.5-flash",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.2
)

# Binary gate for security check
security_gate = Agent(
    name="SecurityGate",
    instructions="""
    Check if the provided code contains any security vulnerabilities.
    Focus on: SQL injection, XSS, hardcoded secrets, unsafe deserialization.
    
    Return JSON:
    {
        "pass": boolean (true if secure, false if vulnerabilities found),
        "reason": string (explanation of decision),
        "details": string (specific vulnerabilities if any)
    }
    """,
    model=model,
    response_format={"type": "json_object"}
)

# Usage in workflow
async def secure_code_workflow(code: str):
    # Run security check
    security_result = await Runner.run(security_gate, code)
    gate_decision = json.loads(security_result.messages[-1].content)
    
    if not gate_decision["pass"]:
        # Block and report
        raise SecurityError(f"Security check failed: {gate_decision['reason']}")
    
    # Proceed with deployment
    return await deploy_code(code)
```

### Complete Rubric Scoring Implementation

```python
# Multi-dimensional content evaluator
content_evaluator = Agent(
    name="ContentEvaluator",
    instructions="""
    Evaluate the technical documentation across multiple dimensions.
    Score each dimension 1-5 (1=poor, 5=excellent).
    
    Return JSON:
    {
        "dimensions": {
            "accuracy": {
                "score": integer,
                "note": string,
                "weight": 0.3
            },
            "completeness": {
                "score": integer,
                "note": string,
                "weight": 0.25
            },
            "clarity": {
                "score": integer,
                "note": string,
                "weight": 0.25
            },
            "examples": {
                "score": integer,
                "note": string,
                "weight": 0.2
            }
        },
        "overall_score": number (weighted average),
        "acceptable": boolean (overall_score >= 3.5),
        "improvement_priority": string (lowest scoring dimension),
        "strengths": [list of high-scoring aspects],
        "weaknesses": [list of low-scoring aspects]
    }
    """,
    model=model,
    response_format={"type": "json_object"}
)

# Usage with improvement loop
async def documentation_improvement_loop(doc: str, max_iterations: int = 3):
    for i in range(max_iterations):
        # Evaluate current version
        eval_result = await Runner.run(content_evaluator, doc)
        evaluation = json.loads(eval_result.messages[-1].content)
        
        if evaluation["acceptable"]:
            return doc, evaluation
        
        # Generate improvements focusing on weaknesses
        doc = await improve_documentation(
            doc, 
            focus_areas=evaluation["weaknesses"],
            priority=evaluation["improvement_priority"]
        )
    
    return doc, evaluation
```

### Complete Differential Evaluation Implementation

```python
# Before/after comparison evaluator
change_evaluator = Agent(
    name="ChangeEvaluator",
    instructions="""
    Compare the original and revised versions of the code.
    Assess whether the changes represent an improvement.
    
    Return JSON:
    {
        "improved": boolean (overall assessment),
        "preserved_strengths": boolean (good parts maintained),
        "new_issues": [
            {
                "issue": string,
                "severity": "low"|"medium"|"high"
            }
        ],
        "fixed_issues": [string (list of resolved problems)],
        "net_better": boolean (considering all factors),
        "improvement_score": number (-1 to 1, negative=worse, positive=better),
        "recommendation": "accept"|"reject"|"revise"
    }
    """,
    model=model,
    response_format={"type": "json_object"}
)

# Usage in code review workflow
async def code_review_workflow(original_code: str, revised_code: str):
    # Evaluate changes
    comparison = await Runner.run(
        change_evaluator,
        f"Original:\n{original_code}\n\nRevised:\n{revised_code}"
    )
    
    diff_eval = json.loads(comparison.messages[-1].content)
    
    if diff_eval["recommendation"] == "accept":
        return revised_code
    elif diff_eval["recommendation"] == "reject":
        return original_code
    else:  # revise
        # Further refinement needed
        return await refine_code(
            revised_code,
            issues=diff_eval["new_issues"],
            preserve=original_code
        )
```

### Complete Compliance Check Implementation

```python
# Regulatory compliance checker
compliance_checker = Agent(
    name="ComplianceChecker",
    instructions="""
    Check if the data processing workflow meets GDPR requirements.
    
    Return JSON:
    {
        "requirements": {
            "consent_mechanism": {
                "met": boolean,
                "evidence": string,
                "notes": string
            },
            "data_minimization": {
                "met": boolean,
                "evidence": string,
                "notes": string
            },
            "right_to_deletion": {
                "met": boolean,
                "evidence": string,
                "notes": string
            },
            "data_portability": {
                "met": boolean,
                "evidence": string,
                "notes": string
            },
            "privacy_by_design": {
                "met": boolean,
                "evidence": string,
                "notes": string
            }
        },
        "fully_compliant": boolean,
        "compliance_percentage": number,
        "missing_requirements": [string],
        "critical_failures": [string (violations that need immediate attention)]
    }
    """,
    model=model,
    response_format={"type": "json_object"}
)

# Usage in compliance workflow
async def gdpr_compliance_workflow(system_design: str):
    compliance_result = await Runner.run(compliance_checker, system_design)
    compliance = json.loads(compliance_result.messages[-1].content)
    
    if compliance["critical_failures"]:
        # Immediate action required
        await alert_legal_team(compliance["critical_failures"])
        raise ComplianceError("Critical GDPR violations found")
    
    if not compliance["fully_compliant"]:
        # Generate remediation plan
        return await create_remediation_plan(
            missing=compliance["missing_requirements"],
            current_design=system_design
        )
    
    return generate_compliance_certificate(compliance)
```

### Complete Criticality Assessment Implementation

```python
# Production readiness critic
readiness_critic = Agent(
    name="ReadinessCritic",
    instructions="""
    Assess the system's readiness for production deployment.
    Categorize issues by severity.
    
    Return JSON:
    {
        "blockers": [
            {
                "issue": string,
                "component": string,
                "fix_required": string,
                "estimated_effort": "hours"|"days"|"weeks"
            }
        ],
        "warnings": [
            {
                "issue": string,
                "suggestion": string,
                "impact": "performance"|"reliability"|"security"|"usability"
            }
        ],
        "info": [string (minor observations)],
        "proceed": boolean (no blockers),
        "priority_fix": string (most critical issue),
        "risk_level": "low"|"medium"|"high"|"critical",
        "deployment_recommendation": string
    }
    """,
    model=model,
    response_format={"type": "json_object"}
)

# Usage in deployment pipeline
async def deployment_readiness_check(system_spec: str):
    readiness = await Runner.run(readiness_critic, system_spec)
    assessment = json.loads(readiness.messages[-1].content)
    
    # Create deployment decision
    deployment_decision = {
        "can_deploy": assessment["proceed"],
        "risk_accepted": assessment["risk_level"] in ["low", "medium"],
        "blockers": assessment["blockers"],
        "pre_deployment_fixes": [],
        "post_deployment_monitors": []
    }
    
    if assessment["blockers"]:
        # Must fix before deployment
        for blocker in assessment["blockers"]:
            deployment_decision["pre_deployment_fixes"].append({
                "issue": blocker["issue"],
                "owner": assign_owner(blocker["component"]),
                "deadline": calculate_deadline(blocker["estimated_effort"])
            })
    
    # Warnings become monitoring points
    for warning in assessment["warnings"]:
        deployment_decision["post_deployment_monitors"].append({
            "metric": derive_metric(warning["issue"]),
            "threshold": derive_threshold(warning["impact"]),
            "alert_channel": get_alert_channel(warning["impact"])
        })
    
    return deployment_decision
```

## Integration Patterns

### Pattern 1: Sequential Evaluation Chain

```python
class EvaluationChain:
    """Chain multiple evaluations in sequence"""
    
    def __init__(self, model):
        self.security_gate = Agent(name="Security", ..., model=model)
        self.quality_scorer = Agent(name="Quality", ..., model=model)
        self.compliance_checker = Agent(name="Compliance", ..., model=model)
    
    async def evaluate(self, artifact):
        # 1. Security gate (must pass)
        security = await self.run_evaluation(self.security_gate, artifact)
        if not security["pass"]:
            return {"rejected": True, "reason": "security", "details": security}
        
        # 2. Quality assessment (must meet threshold)
        quality = await self.run_evaluation(self.quality_scorer, artifact)
        if not quality["acceptable"]:
            return {"rejected": True, "reason": "quality", "details": quality}
        
        # 3. Compliance verification
        compliance = await self.run_evaluation(self.compliance_checker, artifact)
        
        return {
            "approved": compliance["fully_compliant"],
            "evaluations": {
                "security": security,
                "quality": quality,
                "compliance": compliance
            }
        }
```

### Pattern 2: Parallel Evaluation with Aggregation

```python
class ParallelEvaluator:
    """Run multiple evaluations concurrently"""
    
    async def evaluate_parallel(self, artifact):
        # Launch all evaluations concurrently
        evaluations = await asyncio.gather(
            self.run_security_check(artifact),
            self.run_quality_assessment(artifact),
            self.run_performance_test(artifact),
            self.run_accessibility_check(artifact),
            return_exceptions=True
        )
        
        # Aggregate results
        results = {
            "security": evaluations[0],
            "quality": evaluations[1],
            "performance": evaluations[2],
            "accessibility": evaluations[3]
        }
        
        # Determine overall decision
        blockers = []
        warnings = []
        
        for eval_type, result in results.items():
            if isinstance(result, Exception):
                blockers.append(f"{eval_type} evaluation failed: {str(result)}")
            elif not result.get("pass", result.get("acceptable", False)):
                if eval_type in ["security", "performance"]:
                    blockers.append(f"{eval_type}: {result.get('reason', 'Failed')}")
                else:
                    warnings.append(f"{eval_type}: {result.get('reason', 'Suboptimal')}")
        
        return {
            "proceed": len(blockers) == 0,
            "blockers": blockers,
            "warnings": warnings,
            "details": results
        }
```

### Pattern 3: Conditional Evaluation Routing

```python
class ConditionalEvaluator:
    """Route to different evaluations based on content type"""
    
    async def evaluate(self, content, content_type):
        # Determine evaluation strategy
        if content_type == "code":
            evaluations = [
                ("security", self.code_security_check),
                ("quality", self.code_quality_rubric),
                ("performance", self.performance_analysis)
            ]
        elif content_type == "documentation":
            evaluations = [
                ("completeness", self.doc_completeness_check),
                ("clarity", self.readability_scorer),
                ("accuracy", self.technical_accuracy_check)
            ]
        elif content_type == "data":
            evaluations = [
                ("integrity", self.data_integrity_check),
                ("privacy", self.pii_detection),
                ("schema", self.schema_compliance)
            ]
        else:
            evaluations = [("basic", self.basic_quality_check)]
        
        # Run appropriate evaluations
        results = {}
        for name, evaluator in evaluations:
            results[name] = await evaluator(content)
        
        return self.aggregate_results(results, content_type)
```

## Domain-Specific Applications

### Medical Data Generation Evaluation

```python
class MedicalDataEvaluator:
    """Specialized evaluator for medical data generation workflows"""
    
    def __init__(self, model):
        # Phase 1: ICPC-2 Schema Enrichment evaluators
        self.schema_compliance = Agent(
            name="SchemaCompliance",
            instructions="""
            Verify ICPC-2 schema compliance and medical accuracy.
            Return: {
                "requirements": {
                    "valid_icpc2_codes": {"met": bool, "evidence": str},
                    "terminology_accuracy": {"met": bool, "evidence": str},
                    "clinical_consistency": {"met": bool, "evidence": str},
                    "required_fields": {"met": bool, "evidence": str}
                },
                "fully_compliant": bool,
                "medical_concerns": [str]
            }
            """,
            model=model,
            response_format={"type": "json_object"}
        )
        
        self.clinical_reviewer = Agent(
            name="ClinicalReviewer",
            instructions="""
            Review clinical validity and safety of generated content.
            Return: {
                "blockers": [
                    {"issue": str, "clinical_risk": str, "fix_required": str}
                ],
                "warnings": [
                    {"issue": str, "recommendation": str}
                ],
                "proceed": bool,
                "clinical_accuracy_score": float (0-1)
            }
            """,
            model=model,
            response_format={"type": "json_object"}
        )
        
        # Phase 2: Patient Generation evaluators
        self.patient_validator = Agent(
            name="PatientValidator",
            instructions="""
            Validate generated patient data for realism and consistency.
            Return: {
                "dimensions": {
                    "demographic_realism": {"score": int, "note": str},
                    "medical_history_coherence": {"score": int, "note": str},
                    "temporal_consistency": {"score": int, "note": str},
                    "clinical_plausibility": {"score": int, "note": str}
                },
                "acceptable": bool,
                "improvement_priority": str,
                "anonymization_verified": bool
            }
            """,
            model=model,
            response_format={"type": "json_object"}
        )
    
    async def evaluate_schema_enrichment(self, enriched_schema):
        """Evaluate Phase 1: ICPC-2 Schema Enrichment"""
        # Check compliance
        compliance = await Runner.run(self.schema_compliance, enriched_schema)
        comp_data = json.loads(compliance.messages[-1].content)
        
        if not comp_data["fully_compliant"]:
            return {
                "phase": "schema_enrichment",
                "passed": False,
                "retry_with": comp_data["medical_concerns"]
            }
        
        # Clinical review
        clinical = await Runner.run(self.clinical_reviewer, enriched_schema)
        clin_data = json.loads(clinical.messages[-1].content)
        
        return {
            "phase": "schema_enrichment",
            "passed": clin_data["proceed"],
            "compliance": comp_data,
            "clinical": clin_data,
            "next_phase": clin_data["proceed"]
        }
    
    async def evaluate_patient_generation(self, patient_data):
        """Evaluate Phase 2: Patient Generation"""
        validation = await Runner.run(self.patient_validator, patient_data)
        val_data = json.loads(validation.messages[-1].content)
        
        return {
            "phase": "patient_generation",
            "passed": val_data["acceptable"] and val_data["anonymization_verified"],
            "quality_scores": val_data["dimensions"],
            "improvement_needed": val_data["improvement_priority"] if not val_data["acceptable"] else None
        }
```

### Financial Report Evaluation

```python
class FinancialReportEvaluator:
    """Evaluation suite for financial reports and analysis"""
    
    def __init__(self, model):
        self.accuracy_checker = Agent(
            name="AccuracyChecker",
            instructions="""
            Verify numerical accuracy and calculation correctness.
            Return: {
                "calculations_verified": bool,
                "data_sources_validated": bool,
                "discrepancies": [
                    {"location": str, "expected": str, "found": str, "impact": str}
                ],
                "proceed": bool,
                "confidence_score": float
            }
            """,
            model=model,
            response_format={"type": "json_object"}
        )
        
        self.regulatory_compliance = Agent(
            name="RegulatoryCompliance",
            instructions="""
            Check compliance with financial reporting standards (GAAP/IFRS).
            Return: {
                "requirements": {
                    "disclosure_requirements": {"met": bool, "evidence": str},
                    "accounting_standards": {"met": bool, "evidence": str},
                    "audit_trail": {"met": bool, "evidence": str},
                    "material_accuracy": {"met": bool, "evidence": str}
                },
                "fully_compliant": bool,
                "regulatory_risks": [str]
            }
            """,
            model=model,
            response_format={"type": "json_object"}
        )
```

## Best Practices

### 1. Design Evaluation Schemas First

Before implementing agents, design your JSON schemas:

```python
# Define schema as Pydantic model for validation
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class RubricDimension(BaseModel):
    score: int = Field(..., ge=1, le=5)
    note: str
    weight: Optional[float] = Field(None, ge=0, le=1)

class RubricEvaluation(BaseModel):
    dimensions: Dict[str, RubricDimension]
    overall_score: float = Field(..., ge=0, le=5)
    acceptable: bool
    improvement_priority: str
    strengths: List[str]
    weaknesses: List[str]

# Use in agent instructions
instructions = f"""
Evaluate the content and return JSON matching this schema:
{RubricEvaluation.schema_json(indent=2)}
"""
```

### 2. Chain Evaluations Thoughtfully

```python
# Good: Clear evaluation flow with early exits
async def evaluation_pipeline(content):
    # Fast checks first
    format_check = await check_format(content)
    if not format_check["valid"]:
        return {"rejected": True, "stage": "format"}
    
    # Security before quality
    security_check = await check_security(content)
    if not security_check["pass"]:
        return {"rejected": True, "stage": "security"}
    
    # Expensive quality checks last
    quality_check = await check_quality(content)
    return {"approved": quality_check["acceptable"], "quality": quality_check}
```

### 3. Handle Evaluation Failures Gracefully

```python
async def robust_evaluation(agent, content, timeout=30):
    try:
        result = await asyncio.wait_for(
            Runner.run(agent, content),
            timeout=timeout
        )
        return json.loads(result.messages[-1].content)
    except asyncio.TimeoutError:
        return {
            "error": "timeout",
            "fallback_decision": "reject",
            "reason": "Evaluation timed out"
        }
    except json.JSONDecodeError:
        return {
            "error": "invalid_json",
            "fallback_decision": "reject",
            "reason": "Evaluation returned invalid JSON"
        }
    except Exception as e:
        return {
            "error": "unknown",
            "fallback_decision": "reject",
            "reason": str(e)
        }
```

### 4. Provide Context for Better Evaluations

```python
# Good: Rich context for evaluation
evaluation_context = {
    "content": generated_content,
    "requirements": specific_requirements,
    "examples": good_examples,
    "anti_examples": bad_examples,
    "domain_rules": domain_specific_rules
}

result = await evaluator.run(json.dumps(evaluation_context))

# Bad: Just passing content without context
result = await evaluator.run(generated_content)
```

### 5. Log Evaluation Decisions for Debugging

```python
import logging
from datetime import datetime

class EvaluationLogger:
    def __init__(self):
        self.logger = logging.getLogger("evaluations")
    
    async def log_evaluation(self, eval_type, input_hash, result):
        self.logger.info({
            "timestamp": datetime.utcnow().isoformat(),
            "evaluation_type": eval_type,
            "input_hash": input_hash,
            "decision": result.get("pass", result.get("acceptable", False)),
            "scores": result.get("dimensions", {}),
            "blockers": result.get("blockers", []),
            "reasoning": result.get("reason", result.get("improvement_priority"))
        })
```

## Common Pitfalls

### 1. Over-Evaluating

**Problem**: Too many evaluation steps slow down the workflow
**Solution**: Evaluate only at critical decision points

```python
# Bad: Evaluating after every minor step
content = await generate_title()
await evaluate_title(content)  # Unnecessary
content = await add_introduction(content)
await evaluate_intro(content)  # Unnecessary
content = await add_body(content)
await evaluate_body(content)  # Unnecessary

# Good: Evaluate complete artifacts
content = await generate_full_document()
evaluation = await evaluate_document(content)  # One comprehensive evaluation
```

### 2. Vague Evaluation Criteria

**Problem**: Agents can't make consistent decisions with vague instructions
**Solution**: Provide specific, measurable criteria

```python
# Bad: Vague criteria
instructions = "Check if the code is good"

# Good: Specific criteria
instructions = """
Evaluate code quality on these specific criteria:
1. No hardcoded credentials (search for patterns like 'password=', 'api_key=')
2. All functions have docstrings (check function definitions)
3. No TODO comments remain (search for 'TODO', 'FIXME')
4. Error handling exists (try/except blocks present)
Return: {"pass": bool, "violations": [str]}
"""
```

### 3. Ignoring Evaluation Costs

**Problem**: Complex evaluations can be more expensive than generation
**Solution**: Balance thoroughness with cost

```python
class CostAwareEvaluator:
    def __init__(self, budget_tracker):
        self.budget = budget_tracker
    
    async def evaluate(self, content, thoroughness="balanced"):
        if thoroughness == "minimal":
            # Single pass evaluation
            return await self.quick_check(content)
        elif thoroughness == "balanced":
            # Key criteria only
            return await self.standard_check(content)
        elif thoroughness == "comprehensive":
            # Full multi-agent evaluation
            if self.budget.can_afford("comprehensive_eval"):
                return await self.full_evaluation(content)
            else:
                return await self.standard_check(content)
```

### 4. Not Handling JSON Parse Errors

**Problem**: Malformed JSON crashes the workflow
**Solution**: Always wrap JSON parsing with error handling

```python
def safe_parse_evaluation(response):
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        # Fallback evaluation structure
        return {
            "error": "parse_failure",
            "raw_response": response[:200],  # First 200 chars for debugging
            "fallback_decision": "reject",
            "reason": "Evaluation response was not valid JSON"
        }
```

## Quick Reference

### Evaluation Type Selection Flowchart

```
Start
  │
  ├─ Need simple yes/no? ──────────────► BinaryGate
  │   (format valid? authorized?)
  │
  ├─ Comparing versions? ──────────────► DifferentialEvaluation  
  │   (original vs edited?)
  │
  ├─ Fixed requirements? ──────────────► ComplianceCheck
  │   (regulatory? checklist?)
  │
  ├─ Issues have severity? ────────────► CriticalityAssessment
  │   (blockers vs warnings?)
  │
  └─ Need quality score? ──────────────► RubricScoring
      (multi-dimensional assessment)
```

### JSON Response Patterns

```json
// BinaryGate
{"pass": true, "reason": "All checks passed"}

// RubricScoring
{"dimensions": {...}, "acceptable": true, "overall_score": 4.2}

// DifferentialEvaluation
{"improved": true, "net_better": true, "fixed_issues": [...]}

// ComplianceCheck
{"requirements": {...}, "fully_compliant": false, "missing": [...]}

// CriticalityAssessment
{"blockers": [...], "warnings": [...], "proceed": false}
```

### Temperature Settings

- Evaluation agents: `temperature=0.2` (consistency)
- Generation agents: `temperature=0.7` (creativity)
- Critical decisions: `temperature=0.1` (determinism)

### Integration Checklist

- [ ] Define JSON schema for each evaluation type
- [ ] Set temperature=0.2 for all evaluators
- [ ] Add response_format={"type": "json_object"}
- [ ] Implement error handling for JSON parsing
- [ ] Chain evaluations with early exit logic
- [ ] Log evaluation decisions for audit trail
- [ ] Test with malformed inputs
- [ ] Monitor evaluation costs vs generation costs
- [ ] Document evaluation thresholds
- [ ] Create feedback loops for improvements