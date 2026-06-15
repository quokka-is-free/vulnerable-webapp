# [Portfolio] Helix Systems: Vulnerable Web Application for ASM Simulation

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Project Overview

본 프로젝트는 **ASM(Attack Surface Management) 자동화 스캐너**의 성능 검증 및 모의해킹 실습을 위해 구축된 **의도적으로 취약하게 설계된 웹 애플리케이션**입니다. 가상의 기업 'Helix Systems'의 내부 자산으로 가정하며, 실무에서 발생할 수 있는 주요 웹 취약점들을 포함하고 있습니다.

## Key Features & Vulnerabilities

보안 분석 및 자동화 스캔 테스트를 위해 다음과 같은 환경을 구현했습니다.

- **Flask-based Web Architecture**: 가벼운 Flask 프레임워크를 활용한 REST API 및 웹 인터페이스
- **Authentication Vulnerabilities**: 취약한 로그인 로직을 통한 SQL Injection 및 Brute Force 테스트 환경 제공
- **Asset Management Simulation**: Nmap 및 Nuclei 스캔 시 탐지될 수 있는 다양한 포트(80, 22, 5000 등)와 서비스 배너 노출
- **Logging & Monitoring**: 스캔 및 공격 시도에 대한 로그 분석 실습 가능

## Tech Stack

- **Language**: Python 3.x
- **Framework**: Flask
- **Deployment**: systemd 서비스 (Ubuntu 22.04 LTS)
- **Environment**: VMware Workstation Pro 17, Host-only 가상망 (192.168.100.0/24)

## Purpose of Development

1. **ASM 자동화 도구 검증**: 직접 개발한 ASM 스캐너(Nmap/Nuclei 기반)의 취약점 탐지 정확도 테스트
2. **모의해킹 실습**: 실제 환경과 유사한 취약 웹앱을 통해 공격 및 방어 시나리오 수행
3. **인프라 보안 실무**: 실습망(Host-Only) 내 고정 IP 할당 및 네트워크 보안 설정 연습

## Disclaimer

본 프로젝트는 **교육 및 보안 연구 목적**으로만 사용되어야 합니다.

- 모든 테스트는 격리된 가상 환경(VMware Host-only)에서 진행
- 실제 운영 환경 배포 절대 금지
- 정보통신망법 제48조 준수
