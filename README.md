# carinama.scrapy
This is a Scrapy project to scrape name from several Indonesian list name reference site. This project is only meant for learning scraping web site to get an address from it. This is a site that scraped by this repository:
* https://www.prenagen.com/id/kumpulan-nama-bayi
* https://www.popmama.com/baby-name/male/a
* https://www.maknaa.com/arti-nama
* https://kamusnama.com/cari-nama-laki-laki

## Extracted Data
The extracted data will look like this :

### Prenagen
```
{

}
```

### Popmama
```
{
    
}
```

### Maknaa
```
{
    
}
```

### Kamus Nama
```
{
    
}
```

## Usage
Before you can use this repository, you need to install the requirement for this repo. Please type this command in your terminal:

```
$ pip install -r req.txt
```

## Running The Spiders
You can run a spider using the scrapy crawl command, such as:

```
$ scrapy crawl kamusnama_v2
```

If you want to save the scraped data to a file, you can pass the -o option:

```
$ scrapy crawl kamusnama_v2 -o results/kamusnama.json
```