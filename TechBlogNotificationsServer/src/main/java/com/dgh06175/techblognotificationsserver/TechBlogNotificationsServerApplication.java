package com.dgh06175.techblognotificationsserver;

import com.dgh06175.techblognotificationsserver.controller.ScrapController;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

@SpringBootApplication
@EnableJpaAuditing
public class TechBlogNotificationsServerApplication {

    public static void main(String[] args) {
        SpringApplication.run(TechBlogNotificationsServerApplication.class, args);
    }

    @Bean
    CommandLineRunner runScraper(ScrapController scrapController) {
        return args -> {
            scrapController.scrapPosts();
        };
    }
}
