.PHONY: test lint format clean init scan link

# 知识库工具测试和辅助命令

KNOWLEDGE_DIR = tools/knowledge
KNOWLEDGE_SCRIPT = $(KNOWLEDGE_DIR)/knowledge.py

test:
	cd $(KNOWLEDGE_DIR) && python -m pytest test_knowledge.py -v

lint:
	cd $(KNOWLEDGE_DIR) && python -m ruff check knowledge.py test_knowledge.py

format:
	cd $(KNOWLEDGE_DIR) && python -m ruff format knowledge.py test_knowledge.py

init:
	python $(KNOWLEDGE_SCRIPT) init

scan:
	python $(KNOWLEDGE_SCRIPT) scan . src pkg app

check-stale:
	python $(KNOWLEDGE_SCRIPT) check-stale .

reindex:
	python $(KNOWLEDGE_SCRIPT) reindex

lint-kb:
	python $(KNOWLEDGE_SCRIPT) lint

link:
	python $(KNOWLEDGE_SCRIPT) link .

list:
	python $(KNOWLEDGE_SCRIPT) list

clean:
	rm -rf project-knowledge/

help:
	@echo "Available commands:"
	@echo "  test          - Run knowledge tool tests"
	@echo "  lint          - Run ruff check on knowledge tool"
	@echo "  format        - Run ruff format on knowledge tool"
	@echo "  init          - Initialize knowledge base"
	@echo "  scan          - Scan project for exported functions/classes"
	@echo "  check-stale   - Check knowledge entries for staleness"
	@echo "  reindex       - Rebuild INDEX.md from content files"
	@echo "  lint-kb       - Run knowledge base integrity check"
	@echo "  link          - Discover relations between entries"
	@echo "  list          - List all knowledge entries"
	@echo "  clean         - Remove project-knowledge directory"
