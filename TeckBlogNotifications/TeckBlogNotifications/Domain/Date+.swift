//
//  Date+.swift
//  TeckBlogNotifications
//
//  Created by 이상현 on 5/30/24.
//

import Foundation

extension String {
    func parseDate() -> Date {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy. MM. dd"
        guard let parsedDate = formatter.date(from: self) else {
            return Date(timeIntervalSince1970: 0)
        }
        return parsedDate
    }
}

extension Date {
    func formatDate() -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy. MM. dd"
        return formatter.string(from: self)
    }
}
