# Analise Experimental da Hierarquia de Cache e Localidade de Dados sob WSL2

Repositorio de artefatos do artigo cientifico produzido para a disciplina de Infraestrutura de Hardware - CESAR School (2026).

Autor: Marcelo Asfora de Menezes
Orientador: Prof. Ronierison Maciel

## Sobre o projeto

Este trabalho investiga experimentalmente como o tamanho dos dados e o padrao de acesso a memoria impactam a largura de banda e o tempo de execucao em um processador Intel Core i5-1235U executado sob WSL2. Foram conduzidos dois experimentos: medicao de largura de banda com mbw em tres tamanhos de array (16, 128 e 1024 MiB), e comparacao de padroes de acesso sequencial e com saltos sobre uma matriz 3000x3000, com 30 repeticoes cada.

## Como reproduzir

### Requisitos
- Ubuntu 24.04 ou WSL2
- Python 3.12+
- mbw 2.5

### Instalacao
sudo apt install mbw
pip install numpy matplotlib scipy --break-system-packages

### Experimento 1 - MBW
bash run_mbw_30x.sh

### Experimento 2 - Localidade
python3 run_localidade_30x.py

### Analise estatistica
python3 analise_estatistica.py

## Ambiente
- CPU: Intel Core i5-1235U
- Cache: L1d 288 KiB, L2 7.5 MiB, L3 12 MiB
- RAM: 7.6 GiB WSL2
- SO: Ubuntu 24.04 LTS sobre WSL2 Windows 11
