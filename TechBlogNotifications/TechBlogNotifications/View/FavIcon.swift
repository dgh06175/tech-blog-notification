//
//  FavIcon.swift
//  TechBlogNotifications
//
//  Created by 이상현 on 11/22/24.
//

import Foundation

struct FavIcon {
    enum Size: Int, CaseIterable { case s = 16, m = 32, l = 64, xl = 128, xxl = 256, xxxl = 512 }

    // techblog.samsung.com처럼 자체 파비콘 자체가 깨져 있어 도메인 기반으로는 찾을 수 없는
    // 블로그를 위한 수동 예외. blog_name 기준(회사 공식 사이트 아이콘 등으로 직접 지정).
    private static let overrides: [String: String] = [
        "Samsung": "https://www.samsung.com/sec/static/_images/favicon.ico",
    ]

    private let domain: String
    init(_ domain: String) { self.domain = domain }

    private func googleUrl(_ size: Size) -> String {
        "https://www.google.com/s2/favicons?sz=\(size.rawValue)&domain=\(domain)"
    }

    // Google의 favicon 서비스는 못 찾은 도메인에도 (404 상태이지만) 유효한 기본 이미지를 돌려줘서
    // 실패를 감지할 수 없다(예: d2.naver.com은 자체 파비콘이 멀쩡한데도 이 문제로 안 보임). 반면
    // 사이트 자체 favicon.ico는 없거나 깨졌을 때 진짜 실패로 이어지므로, 도메인 자체 favicon.ico를
    // 먼저 시도하고 실패할 때만 Google로 폴백한다.
    // override가 있어도 맨 앞 순위로만 두고 나머지 후보를 함께 반환한다 — override URL이 나중에
    // 깨지거나 옮겨져도 완전히 빈 아이콘이 되지 않고 도메인/Google 순으로 계속 폴백하도록.
    func candidates(blogName: String, size: Size) -> [URL] {
        let overrideUrl = FavIcon.overrides[blogName].flatMap { URL(string: $0) }
        return [
            overrideUrl,
            URL(string: "\(domain)/favicon.ico"),
            URL(string: googleUrl(size)),
        ].compactMap { $0 }
    }
}
