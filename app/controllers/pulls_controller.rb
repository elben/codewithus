class PullsController < ApplicationController
  # GET /pulls
  # GET /pulls.xml
  def index
    @pulls = Pull.all

    respond_to do |format|
      format.html # index.html.erb
      format.xml  { render :xml => @pulls }
    end
  end

  # GET /pulls/1
  # GET /pulls/1.xml
  def show
    @pull = Pull.find(params[:id])

    respond_to do |format|
      format.html # show.html.erb
      format.xml  { render :xml => @pull }
    end
  end

  # GET /pulls/new
  # GET /pulls/new.xml
  def new
    @pull = Pull.new

    respond_to do |format|
      format.html # new.html.erb
      format.xml  { render :xml => @pull }
    end
  end

  # GET /pulls/1/edit
  def edit
    @pull = Pull.find(params[:id])
  end

  # POST /pulls
  # POST /pulls.xml
  def create
    @pull = Pull.new(params[:pull])

    respond_to do |format|
      if @pull.save
        format.html { redirect_to(@pull, :notice => 'Pull was successfully created.') }
        format.xml  { render :xml => @pull, :status => :created, :location => @pull }
      else
        format.html { render :action => "new" }
        format.xml  { render :xml => @pull.errors, :status => :unprocessable_entity }
      end
    end
  end

  # PUT /pulls/1
  # PUT /pulls/1.xml
  def update
    @pull = Pull.find(params[:id])

    respond_to do |format|
      if @pull.update_attributes(params[:pull])
        format.html { redirect_to(@pull, :notice => 'Pull was successfully updated.') }
        format.xml  { head :ok }
      else
        format.html { render :action => "edit" }
        format.xml  { render :xml => @pull.errors, :status => :unprocessable_entity }
      end
    end
  end

  # DELETE /pulls/1
  # DELETE /pulls/1.xml
  def destroy
    @pull = Pull.find(params[:id])
    @pull.destroy

    respond_to do |format|
      format.html { redirect_to(pulls_url) }
      format.xml  { head :ok }
    end
  end
end
