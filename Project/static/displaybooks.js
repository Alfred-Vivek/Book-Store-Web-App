var obj = null;
$(function(){
	$.getJSON('/static/problem-solving-books.json', function(data) {
	    obj=data;
	    window.onload = display();
	});
});
function display(){
	var bookdata=""
	for(var count=0;count<obj.items.length;count+=1){
		bookdata+='<div class="col-md-6">';
		bookdata+='<div class="row well">';
			bookdata+='<div class="col-md-2">';
					bookdata+='<img src='+obj.items[count].volumeInfo.imageLinks.thumbnail+' width="70px" data-toggle="modal" data-target="#myModal'+count+'"></div>'
					bookdata+='<div class="col-md-8">';
							for(var j=0;j<obj.items[count].volumeInfo.authors.length;j+=1){
								bookdata+='<p>'+obj.items[count].volumeInfo.authors[j]+'</p>';
							}
							if(obj.items[count].saleInfo.saleability === 'NOT_FOR_SALE'){
								bookdata+='<p>Price: Not For Sale</p>';
							} else {
								bookdata+='<p>Price: '+obj.items[count].saleInfo.retailPrice.currencyCode+' '+obj.items[count].saleInfo.retailPrice.amount+'</p>'
							}
							bookdata+='<p>Publisher: '+obj.items[count].volumeInfo.publisher+'</p>';
							bookdata+='<p>Publishing date: '+obj.items[count].volumeInfo.publishedDate+'</p>';
					bookdata+='</div>';
					bookdata+='<div class="col-md-2"><button type="button" class="btn btn-info btn-lg" data-toggle="modal" data-target="#myModal'+count+'">Buy</button></div>';
			bookdata+='</div>';
		bookdata+='</div>';
		// Code for the modal.
			bookdata+= '<div class="modal fade" id="myModal'+count+'" role="dialog">'
	    		bookdata+='<div class="modal-dialog modal-lg">'	  
					bookdata+='<div class="modal-content">'
			        bookdata+= '<div class="modal-header">'
			          bookdata+= '<button type="button" class="close" data-dismiss="modal">&times;</button>'
			          bookdata+= '<h4 class="modal-title text-center">'+obj.items[count].volumeInfo.title+'</h4>'
			        bookdata+= '</div>'
			        bookdata+= '<div class="modal-body">'
						bookdata+='<div class="row">';
							bookdata+='<div class="col-sm-2">';	
									bookdata+='<img src='+obj.items[count].volumeInfo.imageLinks.thumbnail+'></div>'
									bookdata+='<div class="col-sm-5">';
											for(var j=0;j<obj.items[count].volumeInfo.authors.length;j+=1){
												bookdata+='<p>'+obj.items[count].volumeInfo.authors[j]+'</p>';
											}
											if(obj.items[count].saleInfo.saleability === 'NOT_FOR_SALE'){
												bookdata+='<p>Price: Not For Sale</p>';
											} else {
												bookdata+='<p>Price: '+obj.items[count].saleInfo.retailPrice.currencyCode+' '+obj.items[count].saleInfo.retailPrice.amount+'</p>'
											}
											bookdata+='<p>Publisher: '+obj.items[count].volumeInfo.publisher+'</p>';
											bookdata+='<p>Publishing date: '+obj.items[count].volumeInfo.publishedDate+'</p>';
										bookdata+='</div>';
										bookdata+='<div class="col-sm-3"><input type="number" class="form-control" name="quantity" min="1" max="3" placeholder="Quantity">';
									bookdata+='<br><center><button type="button" class="btn btn-warning btn-md">Add To Cart</button></center></div>';
									bookdata+='</div>';
									bookdata+='<div class="row">';								
									bookdata+='<div class="col-sm-12">';
									bookdata+='<br><p>Description: '+obj.items[count].volumeInfo.description+'</p>';
									bookdata+='<center><p>Click &nbsp<a href='+obj.items[count].volumeInfo.previewLink+' target="_blank">Here</a>&nbsp for Book Preview</p></center>';
								bookdata+='</div></div></div></div></div></div>';
	}
	document.getElementById("booksList").innerHTML=bookdata;
}