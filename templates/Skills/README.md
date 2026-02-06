# Chimera Agent Skills

Skills are modular capability packages executed by Worker agents.

All Skills MUST:

- Enforce strict input/output contracts
- Use MCP servers for external I/O
- Return structured errors
- Produce auditable evidence

---

## Skill 1: skill_trend_research

### Purpose
Identify trending topics across platforms.

### Input

```json
{
  "platforms": ["x", "tiktok", "instagram"],
  "timeframe": {
    "start_iso": "2026-02-01T00:00:00Z",
    "end_iso": "2026-02-06T00:00:00Z"
  }
}


### Output Contract

{
  "trends": [
    {
      "trend_id": "trend-001",
      "topic": "Malaria prevention awareness",
      "platform": "x",
      "volume": 18200,
      "sentiment": 0.71,
      "evidence": {
        "sample_urls": ["mcp://social/post/9912"],
        "notes": "Spike following WHO announcement"
      }
    }
  ]



}

## Skill 2: skill_content_generate
Purpose
Generate platform-ready content aligned to a trend.

Input

{
  "trend": { "...Trend object..." },
  "content_type": "short_video"
}


Output


{
  "content": {
    "content_id": "content-789",
    "text": "Did you know mosquitoes breed in clean water too?",
    "media_urls": ["mcp://storage/video1.mp4"],
    "metadata": {
      "platform_intent": "tiktok",
      "hashtags": ["#health", "#malaria"],
      "disclosures": ["AI-assisted"]
    },
    "confidence_score": 0.93,
    "safety_tags": ["sensitive:none"]
  }
}


## Skill 3: skill_wallet_operation

Purpose

Perform governed financial actions.

Input

{
  "action_type": "transfer",
  "amount": {
    "value": 50,
    "currency": "USDC"
  },
  "recipient": "wallet_abc123"
}

Output
{
  "receipt": {
    "transaction_id": "tx-456",
    "status": "confirmed",
    "timestamp_iso": "2026-02-06T12:30:00Z",
    "amount": {
      "value": 50,
      "currency": "USDC"
    },
    "recipient": "wallet_abc123",
    "audit_ref": "audit-999"
  }
}

