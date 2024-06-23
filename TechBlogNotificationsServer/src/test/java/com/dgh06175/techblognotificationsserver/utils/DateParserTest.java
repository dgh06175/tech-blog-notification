package com.dgh06175.techblognotificationsserver.utils;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.ValueSource;

import java.time.LocalDate;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatNullPointerException;

public class DateParserTest {

    @ParameterizedTest
    @ValueSource(strings = {"2023-06-23", "2023.06.23", "2023/06/23"})
    void 날짜_구분자가_있는_경우_올바른_날짜_형식(String input) {
        LocalDate expectedDate = LocalDate.parse("2023-06-23");
        assertThat(DateParser.parseDate(input)).isEqualTo(expectedDate);
    }

    @ParameterizedTest
    @CsvSource({
            "'Thu, 20 Jun 2024 00:00:00 GMT', '2024-06-20'",
            "'Fri, 23 Jun 2023 00:00:00 +0000', '2023-06-23'",
            "'Tue, 18 Jun 2024 02:20:05 +0000', '2024-06-18'",
            "'23 Jun 2023', '2023-06-23'",
            "'06/23/2023', 2023-06-23",
            "'23-06-2023', 2023-06-23"
    })
    void 다양한_형식의_날짜_파싱(String input, String expected) {
        LocalDate expectedDate = LocalDate.parse(expected);
        assertThat(DateParser.parseDate(input)).isEqualTo(expectedDate);
    }

    @Test
    void 지원되지_않는_형식의_날짜() {
        String input = "20230623";
        assertThat(DateParser.parseDate(input)).isNull();
    }

    @Test
    void 널_값_입력시_예외() {
        assertThatNullPointerException().isThrownBy(() -> DateParser.parseDate(null));
    }
}
