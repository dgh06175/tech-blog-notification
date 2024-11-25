package com.dgh06175.techblognotificationsserver.exception;

public class ScrapException extends RuntimeException {
    private static final String ERROR_PREFIX = "[ERROR]";

    public ScrapException(String blogUrl) {
        super(String.format("%s %s", ERROR_PREFIX, blogUrl));
    }

    public ScrapException(String blogUrl, ErrorMessage errorMessage) {
        super(String.format("%s %s %s", ERROR_PREFIX, blogUrl, errorMessage.message));
    }
}
