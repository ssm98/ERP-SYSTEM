
from django.db import models
from authentication.models import *
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
# from django.db.models import F
from services.models import *
from authentication.models import *
from django.db.models.signals import pre_save,post_save
import random
import string
User = get_user_model()

paymentChoice=[("STRIPE","stripe"),("WORLDPAY","worldpay"),("CHEQUE","cheque"),("BANK_TRANSFER","bank_transfer"),("CASH","cash")]

class Invoice(models.Model):  # for customers
    user               = models.ForeignKey(User,on_delete=models.CASCADE,null=True,editable=False,blank=True)
    # customer           = models.ForeignKey(Customer, on_delete=models.CASCADE,editable=False,null=True,required=True)
    client_company           = models.ForeignKey(CustomerNew, on_delete=models.CASCADE)
    # from_company           = models.ForeignKey(Company, on_delete=models.CASCADE)
    # from_company       = models.CharField(max_length=20, blank=False, null=True)
    # customer_name      = models.CharField(max_length=20, blank=False, null=True)
    Invoice_number     = models.CharField(max_length=30)  # keep in the format of fisrt customername then date then any serial_number
                                                               # example ; "customername_date_serialnumber"
                                                                # you can use first 2 or 3 letters of every word like
                                                                 # customer: CU, january: JAN,
                                                                  # serial number: numerals like 123,

    Invoice_date           = models.DateField()
    payment_terms          = models.CharField(max_length=100,choices=paymentChoice,blank=False) 
  
    service                = models.ForeignKey(Service, on_delete=models.CASCADE, null=False,blank=False)
    description            = models.TextField(max_length=250, blank=True, null=True)    
    rate                   = models.FloatField(blank=True, null=True,default=0)
    Qty                    = models.FloatField(blank=True, null=True,default=0)
    Discount               = models.FloatField(blank=True, null=True,default=0)
    Tax                    = models.FloatField(blank=True, null=True,default=0)
    Total                  = models.FloatField(blank=True, null=True,default=0)
   

    def __str__(self):
        return str(self.client_company.company_name)
    class Meta:
        verbose_name_plural = 'invoice'


#instance,sender,created,*args,**kwargs
#from
def random_string_generator(size=7,char=string.ascii_lowercase+string.digits):
    return ''.join(random.choice(char) for _ in range(size))

def invoice_no_generator(instance,sender,*args, **kwargs):
    if not instance.Invoice_number:
        word="INV"
        instance.Invoice_number= word+"_"+str(instance.client_company.company_name)+"_"+str(random_string_generator())


pre_save.connect(invoice_no_generator,sender=Invoice)

#def po_no_generator(instance,sender,*args, **kwargs):
#    if not instance.PO_Number:
#        word="PO"
#        instance.PO_Number= word+"_"+str(instance.Vendor.company_Name)+"_"+str(random_string_generator())

#pre_save.connect(po_no_generator,sender=PurchaseOrder)

#to
def post_save_Stotal(instance,sender,*args,**kwargs):

    inst_rate=instance.rate
    inst_Qty=instance.Qty
    inst_Discount=instance.Discount
    inst_Tax=instance.Tax
    saDis=inst_rate*inst_Qty*(inst_Discount/100)
    # pricewithdiscount=inst_rate*inst_Qty-saDis
    # pricewithtax=inst_rate*inst_Qty+saTax
# jk
    #inst_Total = instance.Total
    inst_Total=0

    priceafterdis=((inst_rate*inst_Qty)-saDis)
    print('priceafterdis',priceafterdis)

    saTax=priceafterdis*(inst_Tax/100)
    print(saTax)
    #inst_Total+=priceafterdis+saTax
    instance.Total=priceafterdis+saTax
    # inst_Total = 0
    
    # inst_Total += ((inst_rate *  inst_Qty) - (((inst_Discount)/100) * ( inst_Qty * inst_rate)) + inst_Tax)
    print(inst_Total)
    q=inst_Total
    print(q)
    #instance.save()
    #Invoice.objects.filter(pk=instance.pk).update(Total=q)  
    
   

pre_save.connect(post_save_Stotal, sender=Invoice)



class ServiceEntry(models.Model):
    # invoice                = models.ForeignKey(Invoice,on_delete=models.CASCADE,null=True,related_name="invoice_link")
    # service                = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    description            = models.TextField(max_length=250, blank=False, null=True)    
    rate                   = models.FloatField()
    Qty                    = models.FloatField()
    Discount               = models.FloatField()
    Tax                    = models.FloatField()

    

    def __str__(self):
        return str(self.description)  
        



    ##################################################################################

    def save(self,*args,**kwargs):       ################ WILL NOT WORK IF YOU GOING TO INITIALIZE FIRST OBJECT
        # super(ServiceEntry,self).save(*args, **kwargs)
        invoice = Invoice.objects.get(id=self.id)
        entries = invoice.serviceentry_set.all()
        self.Total = 0
        for q in entries.iterator():
            self.Total += ((q.rate * q.Qty) - (((q.Discount)/100) * (q.Qty * q.rate)) + q.Tax )

        # print(self.Total)
        super(Invoice,self).save(*args, **kwargs)




    
class PurchaseOrder(models.Model):  # for vendors
    # Vendor                 = models.ForeignKey(Vendor, on_delete=models.CASCADE,)
    # client_company                 = models.ForeignKey(Company, on_delete=models.CASCADE,)
    Vendor                 = models.ForeignKey(VendorNew, on_delete=models.CASCADE)
    # vendor_name            = models.CharField(max_length=50, blank=False, null=True)
    # date_time              = models.DateTimeField(verbose_name ='date and time of Purchasing Order',
    #                                               auto_now=False, auto_now_add=True)  
    PO_Number              = models.CharField(max_length=50)  # keep in the format of fisrt vendorname 
                                                               # then date then any serial_number
                                                                # example ; "customername_date_serialnumber"
                                                                 # you can use first 2 or 3 letters of every word like
                                                                  # customer: CU, january: JAN,
                                                                   # serial number: numerals like 123,

    # vendor_sn              = models.CharField(verbose_name = 'vendorID',max_length=20, blank=False,
                                            # null=True)  # format :- first client_name then vendor_name
    PO_Date                = models.DateField()
    service                = models.ForeignKey(Service, on_delete=models.CASCADE, null=True,blank=True)
    description            = models.TextField(max_length=250, blank=True, null=True)
    rate                   = models.FloatField(blank=True, null=True)    
    Qty                    = models.FloatField(blank=True, null=True)
    Discount               = models.FloatField(blank=True, null=True)
    Tax                    = models.FloatField(blank=True, null=True)
    Total                  = models.FloatField(blank=True, null=True,default=0)



    def __str__(self):
        return self.Vendor.company_name

    class Meta:
        verbose_name_plural = 'purchaseOrder'

def post_save_Ptotal(instance,sender,*args,**kwargs):

    inst_rate=instance.rate
    inst_Qty=instance.Qty
    inst_Discount=instance.Discount
    inst_Tax=instance.Tax
    # dd
    saDis=inst_rate*inst_Qty*(inst_Discount/100)
    # pricewithdiscount=inst_rate*inst_Qty-saDis
    # pricewithtax=inst_rate*inst_Qty+saTax
# jk
    #inst_Total=instance.Total
    inst_Total = 0

    priceafterdis=((inst_rate*inst_Qty)-saDis)
    print('priceafterdis',priceafterdis)

    saTax=priceafterdis*(inst_Tax/100)
    print(saTax)
    #inst_Total+=priceafterdis+saTax
    instance.Total=priceafterdis+saTax
    # inst_Total += ((inst_rate *  inst_Qty) - (((inst_Discount)/100) * ( inst_Qty * inst_rate)) + inst_Tax)
    print(inst_Total)
    q=inst_Total
    print(q)

def po_no_generator(instance,sender,*args, **kwargs):
    if not instance.PO_Number:
        word="PO"
        instance.PO_Number= word+"_"+str(instance.Vendor.company_name)+"_"+str(random_string_generator())

pre_save.connect(po_no_generator,sender=PurchaseOrder)

#    PurchaseOrder.objects.filter(pk=instance.pk).update(Total=q)  
    
   

pre_save.connect(post_save_Ptotal, sender=PurchaseOrder)

    
# def pre_save_Ptotal(instance,sender,*args,**kwrags):
#     # invoice = Invoice.objects.get(id=instance.id)
#     entries = instance.productentry_set.all()
#     instance.Total = 0
#     for q in entries.iterator():
#         instance.Total += ((q.rate * q.Qty) - (((q.Discount)/100) * (q.Qty * q.rate)) + q.Tax)
#
# pre_save.connect(pre_save_Ptotal, sender=PurchaseOrder)


    # def save(self,*args,**kwargs):    ################ WILL NOT WORK IF YOU GOING TO INITIALIZE FIRST OBJECT
    #     po = PurchaseOrder.objects.get(id=self.id)
    #     entries = po.productentry_set.all()
    #     self.PTotal = 0
    #     for q in entries.iterator():
    #         self.PTotal += ((q.rate * q.Qty) - (((q.Discount)/100) * (q.Qty * q.rate)) + q.Tax )
        
    
    #     super(PurchaseOrder,self).save(*args, **kwargs)




#                                                             #--------------------FOR PRODUCT INLINE
# class ProductEntry(models.Model):
#     PO                     = models.ForeignKey(PurchaseOrder,on_delete=models.CASCADE,null=True,related_name="product_link")
#     Product                = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
#     description            = models.TextField(max_length=250, blank=False, null=True)
#     rate                   = models.FloatField()    
#     Qty                    = models.FloatField()
#     Discount               = models.FloatField()
#     Tax                    = models.FloatField()

#     # payment_terms          = models.TextField(max_length=250, blank=False, null=True)

#     def __str__(self):
#         return str(self.Product)


class JournalEn(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=False)
    particular = models.CharField(max_length=50)
    debit = models.IntegerField(blank=True, null=True, )    
    credit = models.IntegerField(blank=True, null=True, ) 

    def __str__(self):
        return self.particular

class PaymentEn(models.Model):   
    date = models.DateField(auto_now=False, auto_now_add=False)
    particular = models.CharField(max_length=50)
    debit = models.IntegerField(blank=True, null=True, )    
    credit = models.IntegerField(blank=True, null=True, ) 
    def __str__(self):
        return self.particular
   
class ContraEn(models.Model):   
    date = models.DateField(auto_now=False, auto_now_add=False)
    particular = models.CharField(max_length=50)
    debit = models.IntegerField(blank=True, null=True, )    
    credit = models.IntegerField(blank=True, null=True, )
   
    def __str__(self):
        return self.particular

class ReceiptEn(models.Model):   
    date= models.DateField(auto_now=False, auto_now_add=False)
    particular = models.CharField(max_length=50)
    debit = models.IntegerField(blank=True, null=True, )    
    credit = models.IntegerField(blank=True, null=True, )
    
    def __str__(self):
        return self.particular

class Ledger(models.Model):
    name = models.CharField(max_length=50)
    amount = models.CharField(max_length=50)
    dep = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    


