package com.dgh06175.techblognotificationsserver.config;

import com.dgh06175.techblognotificationsserver.domain.Post;
import org.jsoup.nodes.Element;

public interface BlogConfig {
    String getBlogName();
    String getBlogUrl();
    String getListTagName();
    Post parseElement(Element element);
}
