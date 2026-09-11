# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: tiana-an <tiana-an@student.42antananari    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/08/27 09:03:59 by tiana-an          #+#    #+#              #
#    Updated: 2026/09/11 09:03:02 by tiana-an         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

C_RESET		= \033[0m
C_GREEN		= \033[032m
C_BLUE		= \033[034m

export UV_CACHE_DIR=$(HOME)/goinfre/caches
export HF_HOME=$(HOME)/goinfre/caches

RM = rm -rf
MYPY_FLAGS = \
	--warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs

all: run

install:
	@echo "${C_BLUE}Installing dependencies...\n${C_RESET}"
	@uv sync

run:
	@uv run python3 -m src

debug:
	@uv run python3 -m pdb -m src

clean:
	@echo "${C_BLUE}Removing temporary files or caches...\n${C_RESET}"
	@find . -type d -name "__pycache__" -exec $(RM) {} +
	@find . -type d -name ".mypy_cache" -exec $(RM) {} +
	@echo "${C_GREEN}Our project environment is clean\n${C_RESET}"

lint:
	@echo "${C_BLUE}Running flake8 src/ ...\n${C_RESET}"
	@uv run flake8 src/
	@echo "${C_BLUE}Running mypy with custom flags...\n${C_RESET}"
	@uv run mypy src/ $(MYPY_FLAGS)

lint-strict:
	@echo "${C_BLUE}Running flake8 src/...\n${C_RESET}"
	@uv run flake8 src/
	@echo "${C_BLUE}Running mypy --strict...\n${C_RESET}"
	@uv run mypy --strict src/

.PHONY: all install run debug clean lint lint-strict
