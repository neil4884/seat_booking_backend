class command :
    #check in -> front ส่ง0->1 ปะวะ 
    #back ต้องทำปะวะ
    #front ส่งอะไรมาอะว่าคนนี้ติ๊ด qr แล้ว
    def check_in(id) :
        user.find(id).set_status(1)
        
        #if user.find(id).get_status == 2 :


    #check out มี 2 แบบ
    #extend=0 เมื่อไม่มี request extend
    #extend=time เมื่อมี request extend และกด pop cat ได้ตามจำนวน time
    def check_out(id,extend) :
        if (extend==0) : #ออกไปแล้วจะนับถอยหลังเวลายังไง? เวลามันจะนับถอยหลังทุกนาทียังไง?
            user.find(id).set_status(0)
        else :
            user.find(id).set_status(2)

    



        
    

 