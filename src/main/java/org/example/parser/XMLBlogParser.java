package org.example.parser;

import org.example.model.Article;
import org.jsoup.nodes.Element;


public class XMLBlogParser extends AbstractJsoupBlogParser {
    @Override
    protected String getItemTagName() {
        return "item";
    }

    @Override
    protected Article parseElement(Element element) {
        String link = element.select("link").text();
        String title = element.select("title").text();
        String author = element.select("dc\\:creator").text();
        String date = element.select("pubDate").text();

        return new Article(link, title, author, date);
    }
}
