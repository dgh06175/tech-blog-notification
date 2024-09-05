package com.dgh06175.techblognotificationsscrapper.exception;

import static com.dgh06175.techblognotificationsscrapper.exception.ErrorMessage.SCRAP_NULL_DOCUMENT;

public class ScrapHttpException extends ScrapException {

    public ScrapHttpException(String blogUrl) {
        super(blogUrl, SCRAP_NULL_DOCUMENT);
    }
}
