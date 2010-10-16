class CheckoutsController < ApplicationController
  # GET /checkouts
  # GET /checkouts.xml
  def index
    @checkouts = Checkout.all

    respond_to do |format|
      format.html # index.html.erb
      format.xml  { render :xml => @checkouts }
    end
  end

  # GET /checkouts/1
  # GET /checkouts/1.xml
  def show
    @checkout = Checkout.find(params[:id])

    respond_to do |format|
      format.html # show.html.erb
      format.xml  { render :xml => @checkout }
    end
  end

  # GET /checkouts/new
  # GET /checkouts/new.xml
  def new
    @checkout = Checkout.new

    respond_to do |format|
      format.html # new.html.erb
      format.xml  { render :xml => @checkout }
    end
  end

  # GET /checkouts/1/edit
  def edit
    @checkout = Checkout.find(params[:id])
  end

  # POST /checkouts
  # POST /checkouts.xml
  def create
    @checkout = Checkout.new(params[:checkout])

    respond_to do |format|
      if @checkout.save
        format.html { redirect_to(@checkout, :notice => 'Checkout was successfully created.') }
        format.xml  { render :xml => @checkout, :status => :created, :location => @checkout }
      else
        format.html { render :action => "new" }
        format.xml  { render :xml => @checkout.errors, :status => :unprocessable_entity }
      end
    end
  end

  # PUT /checkouts/1
  # PUT /checkouts/1.xml
  def update
    @checkout = Checkout.find(params[:id])

    respond_to do |format|
      if @checkout.update_attributes(params[:checkout])
        format.html { redirect_to(@checkout, :notice => 'Checkout was successfully updated.') }
        format.xml  { head :ok }
      else
        format.html { render :action => "edit" }
        format.xml  { render :xml => @checkout.errors, :status => :unprocessable_entity }
      end
    end
  end

  # DELETE /checkouts/1
  # DELETE /checkouts/1.xml
  def destroy
    @checkout = Checkout.find(params[:id])
    @checkout.destroy

    respond_to do |format|
      format.html { redirect_to(checkouts_url) }
      format.xml  { head :ok }
    end
  end
end
