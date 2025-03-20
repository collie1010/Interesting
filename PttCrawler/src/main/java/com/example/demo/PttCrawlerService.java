package com.example.demo;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@Service
public class PttCrawlerService {
    
    private static final String PTT_URL = "https://www.ptt.cc";
    private static final Logger logger = LoggerFactory.getLogger(PttCrawlerService.class);
    
    public List<ArticleDTO> crawlBoard(String boardName) throws IOException {
        // 建立連線並設定 cookie 以避免年齡確認
        Document doc = Jsoup.connect(PTT_URL + "/bbs/" + boardName + "/index.html")
                .cookie("over18", "1")
                .get();
                
        List<ArticleDTO> articles = new ArrayList<>();
        Elements rows = doc.select("div.r-ent");
        
        for (Element row : rows) {
            ArticleDTO article = new ArticleDTO();
            
            // 取得標題
            Element titleElement = row.select("div.title a").first();
            if (titleElement != null) {
                article.setTitle(titleElement.text());
                article.setLink(PTT_URL + titleElement.attr("href"));
            }
            
            // 取得作者
            Element authorElement = row.select("div.meta div.author").first();
            if (authorElement != null) {
                article.setAuthor(authorElement.text());
            }
            
            // 取得日期
            Element dateElement = row.select("div.meta div.date").first();
            if (dateElement != null) {
                article.setDate(dateElement.text().trim());
            }
            
            if (titleElement != null) {  // 只加入有標題的文章
                articles.add(article);
            }
        }
        
        logger.info("PttCrawler crawled board {} successfully", boardName.toUpperCase());
        
        return articles;
    }
}
