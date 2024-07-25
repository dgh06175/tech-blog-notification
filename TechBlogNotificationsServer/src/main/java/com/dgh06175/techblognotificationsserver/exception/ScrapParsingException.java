package com.dgh06175.techblognotificationsserver.exception;

import static com.dgh06175.techblognotificationsserver.exception.ErrorMessage.SCRAP_EMPTY_PARSED_DATA;

public class ScrapParsingException extends ScrapException {
    public ScrapParsingException(String blogUrl) {
        super(blogUrl, SCRAP_EMPTY_PARSED_DATA);
    }
}