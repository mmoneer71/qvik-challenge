sample_index_message = {"message": "Some message"}

sample_channel = {"id": 1, "name": "Science"}

sample_channel_list = [{"id": 1, "name": "Science"}, {"id": 2, "name": "Fiction"}, {"id": 3, "name": "Romance"}]

sample_404 = {"detail": "Not found"}

sample_422 = {"detail":[{"loc":["path","channel_id"],"msg":"value is not a valid integer","type":"type_error.integer"}]}

sample_article = {"id": 1, "url": "http://example.com/article1.html", "word_count": 150, "channel_id": 1}

sample_article_list = [{"id": 1, "url": "http://example.com/article1.html", "word_count": 150, "channel_id": 1}, 
{"id": 2, "url": "http://example.com/article2.html", "word_count": 250, "channel_id": 1}, ]

sample_bckgrnd = "Article will be fetched and created in the background"

sample_urls = ["https://edition.cnn.com/2020/09/21/us/arctic-sea-ice-shrunk-minimum-extent-2020-scn-trnd/index.html",
                "https://edition.cnn.com/2021/10/06/us/gabby-petito-brian-laundrie-update-wednesday/index.html"]
