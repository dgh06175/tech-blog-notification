package com.dgh06175.techblognotificationsserver.utils;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.Arrays;
import java.util.List;
import java.util.Locale;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


public class DateParser {
    private static final String ERROR_PREFIX = "[ERROR]";
    private static final Pattern SIMPLE_DATE_PATTERN = Pattern.compile("(\\d{4})\\D+(\\d{1,2})\\D+(\\d{1,2})");
    private static final Logger logger = LoggerFactory.getLogger(DateParser.class.getName());

    // MARK: - 새로운 날짜 형식이 발견되면 이 부분에 알맞은 패턴 문자열 추가
    private static final List<DateTimeFormatter> DATE_FORMATTERS = Arrays.asList(
            DateTimeFormatter.ofPattern("EEE, dd MMM yyyy HH:mm:ss Z", Locale.ENGLISH),
            DateTimeFormatter.ofPattern("EEE, dd MMM yyyy HH:mm:ss z", Locale.ENGLISH),
            DateTimeFormatter.ofPattern("d MMM yyyy", Locale.ENGLISH),
            DateTimeFormatter.ofPattern("MM/dd/yyyy"),
            DateTimeFormatter.ofPattern("dd-MM-yyyy"),
            DateTimeFormatter.ISO_DATE,
            DateTimeFormatter.ISO_DATE_TIME,
            DateTimeFormatter.ISO_OFFSET_DATE,
            DateTimeFormatter.ISO_OFFSET_DATE_TIME
    );

    public static LocalDate parseDate(String dateString) {
        for (DateTimeFormatter formatter : DATE_FORMATTERS) {
            try {
                return LocalDate.parse(dateString, formatter);
            } catch (DateTimeParseException ignored) {}
        }

        // 구분자가 있는 보편적인 날짜 형식 추출
        Matcher matcher = SIMPLE_DATE_PATTERN.matcher(dateString);
        if (matcher.find()) {
            String extractedDate = String.format("%s-%s-%s", matcher.group(1), matcher.group(2), matcher.group(3));
            try {
                return LocalDate.parse(extractedDate, DateTimeFormatter.ofPattern("yyyy-M-d"));
            } catch (DateTimeParseException e) {
                logger.info(String.format("%s %s: %s", ERROR_PREFIX, "파싱 예외 발생. null 반환", dateString));
            }
        }

        logger.info(String.format("%s %s: %s", ERROR_PREFIX, "파싱 형식 매칭 실패. null 반환", dateString));
        return null;
    }
}