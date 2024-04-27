package org.example.parser;

import org.example.model.Articles;

public interface ParserStrategy {
    Articles parse(String url, String blogName);
}
