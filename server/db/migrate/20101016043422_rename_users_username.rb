class RenameUsersUsername < ActiveRecord::Migration
  def self.up
    rename_column :users, :username, :email
    add_column :users, :name, :string
  end

  def self.down
    remove_column :users, :name
    rename_column :users, :email, :username
  end
end
