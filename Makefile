.PHONY: install test lint clean providers presets \
        music-jazz music-blues music-ethiopian music-cinematic music-electronic music-lofi music-custom music-minimax \
        video-nature video-space video-urban video-fantasy video-custom video-kling \
        help jobs jobs-stats jobs-sync


# =========================================
# AI Content Generation Package
# =========================================

# --- Setup ---
install:
	uv sync
	@echo "✅ ai-content package installed"
install-docker:
	docker run --rm -it -v $(PWD):/app ai_swarm uv sync
	@echo "✅ ai-content package installed"

test-local:
	uv run pytest tests/

test-docker:
	docker run --rm -it -v $(PWD):/app ai_swarm pytest tests/

lint:
	uv run ruff check src/
	uv run mypy src/

clean:
	rm -rf exports/* __pycache__/ .ruff_cache/ .mypy_cache/

# --- CLI Commands ---
providers:
	uv run ai-content list-providers

presets:
	uv run ai-content list-presets

# --- Music Generation (New CLI) ---
music-jazz:
	uv run ai-content music --style jazz --provider lyria

music-blues:
	uv run ai-content music --style blues --provider lyria

music-ethiopian:
	uv run ai-content music --style ethiopian-jazz --provider lyria

music-cinematic:
	uv run ai-content music --style cinematic --provider lyria

music-electronic:
	uv run ai-content music --style electronic --provider lyria

music-lofi:
	uv run ai-content music --style lofi --provider lyria

music-custom:
	@echo "Usage: make music-custom PROMPT='your prompt' PROVIDER=lyria"
	uv run ai-content music --prompt "$(PROMPT)" --provider $(PROVIDER)

# --- Video Generation (New CLI) ---
video-nature:
	uv run ai-content video --style nature --provider veo

video-space:
	uv run ai-content video --style space --provider veo

video-urban:
	uv run ai-content video --style urban --provider veo

video-fantasy:
	uv run ai-content video --style fantasy --provider veo

video-custom:
	@echo "Usage: make video-custom PROMPT='your prompt' PROVIDER=veo"
	uv run ai-content video --prompt "$(PROMPT)" --provider $(PROVIDER)

# --- High Quality Video (Kling - 5-14min) ---
video-kling:
	@echo "⏳ KlingAI takes 5-14 minutes..."
	uv run ai-content video --style fantasy --provider kling

# --- Music with MiniMax (vocals support) ---
music-minimax:
	uv run ai-content music --style jazz --provider minimax

# --- Help ---
help:
	@echo "=============================================="
	@echo "AI Content Generation"
	@echo "=============================================="
	@echo ""
	@echo "📦 Setup:"
	@echo "  make install        - Install package"
	@echo "  make test           - Run tests"
	@echo "  make lint           - Run linting"
	@echo "  make clean          - Clean caches"
	@echo ""
	@echo "📋 Discovery:"
	@echo "  make providers      - List all providers"
	@echo "  make presets        - List all presets"
	@echo ""
	@echo "🎵 Music (Lyria - Instrumental):"
	@echo "  make music-jazz     - Smooth jazz (95 BPM)"
	@echo "  make music-blues    - Delta blues (72 BPM)"
	@echo "  make music-ethiopian - Ethio-Jazz (85 BPM)"
	@echo "  make music-cinematic - Epic orchestral"
	@echo "  make music-electronic - Progressive house"
	@echo "  make music-lofi     - Lo-fi hip-hop"
	@echo ""
	@echo "🎵 Music (MiniMax - Vocals):"
	@echo "  make music-minimax  - Jazz with vocals"
	@echo ""
	@echo "🎬 Video (Veo - Fast ~30s):"
	@echo "  make video-nature   - Wildlife documentary"
	@echo "  make video-space    - Sci-fi astronaut"
	@echo "  make video-urban    - Cyberpunk city"
	@echo "  make video-fantasy  - Epic fantasy"
	@echo ""
	@echo "🎬 Video (Kling - High Quality, 5-14min):"
	@echo "  make video-kling    - Fantasy (highest quality)"
	@echo ""
	@echo "📊 Job Tracking:"
	@echo "  make jobs           - List tracked jobs"
	@echo "  make jobs-stats     - View job statistics"
	@echo "  make jobs-sync      - Sync pending job status"
	@echo ""
	@echo "🛠️ Custom Generation:"
	@echo "  make music-custom PROMPT='jazz fusion' PROVIDER=lyria"
	@echo "  make video-custom PROMPT='dragon flying' PROVIDER=veo"
	@echo ""
	@echo "📖 Direct CLI:"
	@echo "  uv run ai-content --help"
	@echo "  uv run ai-content music --help"
	@echo "  uv run ai-content video --help"
	@echo ""
	@echo "📘 Docs: docs/architecture/ARCHITECTURE.md"
	@echo ""

# --- Job Tracking ---
jobs:
	uv run ai-content jobs

jobs-stats:
	uv run ai-content jobs-stats

jobs-sync:
	uv run ai-content jobs-sync --download
