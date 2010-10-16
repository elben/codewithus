class PushesController < ApplicationController
  # GET /pushes
  # GET /pushes.xml
  def index
    @pushes = Push.all

    respond_to do |format|
      format.html # index.html.erb
      format.xml  { render :xml => @pushes }
    end
  end

  # GET /pushes/1
  # GET /pushes/1.xml
  def show
    @push = Push.find(params[:id])

    respond_to do |format|
      format.html # show.html.erb
      format.xml  { render :xml => @push }
    end
  end

  # GET /pushes/new
  # GET /pushes/new.xml
  def new
    @push = Push.new

    respond_to do |format|
      format.html # new.html.erb
      format.xml  { render :xml => @push }
    end
  end

  # GET /pushes/1/edit
  def edit
    @push = Push.find(params[:id])
  end

  # POST /pushes
  # POST /pushes.xml
  def create
    @push = Push.new(params[:push])

    respond_to do |format|
      if @push.save
        format.html { redirect_to(@push, :notice => 'Push was successfully created.') }
        format.xml  { render :xml => @push, :status => :created, :location => @push }
      else
        format.html { render :action => "new" }
        format.xml  { render :xml => @push.errors, :status => :unprocessable_entity }
      end
    end
  end

  # PUT /pushes/1
  # PUT /pushes/1.xml
  def update
    @push = Push.find(params[:id])

    respond_to do |format|
      if @push.update_attributes(params[:push])
        format.html { redirect_to(@push, :notice => 'Push was successfully updated.') }
        format.xml  { head :ok }
      else
        format.html { render :action => "edit" }
        format.xml  { render :xml => @push.errors, :status => :unprocessable_entity }
      end
    end
  end

  # DELETE /pushes/1
  # DELETE /pushes/1.xml
  def destroy
    @push = Push.find(params[:id])
    @push.destroy

    respond_to do |format|
      format.html { redirect_to(pushes_url) }
      format.xml  { head :ok }
    end
  end
end
