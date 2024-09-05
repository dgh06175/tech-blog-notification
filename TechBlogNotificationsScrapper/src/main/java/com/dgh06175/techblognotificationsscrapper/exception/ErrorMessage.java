package com.dgh06175.techblognotificationsscrapper.exception;

public enum ErrorMessage {
    SCRAP_UNKNOWN_HOST_EXCEPTION("UnknownHost 예외 발생. 네트워크 상태를 확인해주세요."),
    SCRAP_NULL_DOCUMENT("URL 응답이 비어있습니다. 해당 블로그의 URL 문자열이 올바른지 확인해주세요."),
    SCRAP_EMPTY_PARSED_DATA("파싱한 데이터가 비어있습니다. getListTagName 또는 파싱 로직이 올바른지 확인해주세요.");

    public final String message;

    ErrorMessage(String message) {
        this.message = message;
    }
}
