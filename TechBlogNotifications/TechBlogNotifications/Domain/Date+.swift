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
        formatter.dateFormat = Constants.DateFormat.YEAR_MONTH_DAY_DATEFORMAT
        guard let parsedDate = formatter.date(from: self) else {
            return Date(timeIntervalSince1970: 0)
        }
        return parsedDate
    }
}

extension Date {
    func formatDateToYearMonthDay() -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = Constants.DateFormat.YEAR_MONTH_DAY_DATEFORMAT
        return formatter.string(from: self)
    }
    
    func formatDateToYearMonth() -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = Constants.DateFormat.YEAR_MONTH_DATEFORMAT
        return formatter.string(from: self)
    }
}
