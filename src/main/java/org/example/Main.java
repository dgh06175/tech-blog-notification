package org.example;

import org.example.model.DataManager;
import org.example.parser.TossHTMLBlogParser;
import org.example.parser.XMLBlogParser;

public class Main {
    public static void main(String[] args) {
        new BlogController(new DataManager(), new XMLBlogParser(), new TossHTMLBlogParser()).run();
    }
}