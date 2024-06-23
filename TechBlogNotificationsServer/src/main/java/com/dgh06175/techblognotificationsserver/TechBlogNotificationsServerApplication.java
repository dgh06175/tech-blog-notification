package com.dgh06175.techblognotificationsserver;

import com.dgh06175.techblognotificationsserver.controller.ScrapController;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class TechBlogNotificationsServerApplication {

    public static void main(String[] args) {
//        SpringApplication.run(TechBlogNotificationsServerApplication.class, args);
        new ScrapController().run();
    }
}
